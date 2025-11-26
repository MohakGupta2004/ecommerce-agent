import logging
from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    JobProcess,
    MetricsCollectedEvent,
    RoomInputOptions,
    WorkerOptions,
    cli,
    metrics,
    tokenize,
    function_tool,
    RunContext
)
import json
import os
from livekit.plugins import murf, silero, google, deepgram, noise_cancellation
from livekit.plugins.turn_detector.multilingual import MultilingualModel
import re
from datetime import datetime

logger = logging.getLogger("agent")

load_dotenv(".env")


class Assistant(Agent):
    def __init__(self, faq_data: dict = None) -> None:
        self.faq_data = faq_data or {}
        super().__init__(
            instructions="""
    You are Hazel, a Sales Development Representative (SDR) voice agent for Zerodha. Your primary goals:
    - Professionally answer basic company questions using the FAQ data available to you (products, pricing ranges, integrations, support hours, website, and high-level differentiators).
    - Qualify and capture lead information reliably and politely.
    - At call end, produce a concise call summary and a structured lead record (JSON) with recommended next steps.
    
    IMPORTANT: You have access to company FAQ data through the get_faq_info tool. Use it to answer questions about company details, products, pricing, and services.

    Behavior and tone:
    - Be friendly, professional, succinct, and conversational. Use short sentences for clear TTS output.
    - Ask one question at a time. Confirm and repeat critical contact details back to the prospect to verify accuracy.
    - Use active listening: reflect key points, confirm pain points and timeline.
    - Never request or record sensitive personal information (e.g., SSN, credit card numbers). If a prospect offers such details, politely decline and state you cannot collect that info.

    Qualifying flow (example sequence, adapt as needed):
    1. Quick intro and reason for calling.
    2. Confirm prospect identity and role.
    3. Ask open questions to identify pain points and current solutions.
    4. Ask about decision authority and timeline.
    5. Ask about estimated budget range (if comfortable).
    6. Confirm best email and phone for follow-up and permission to send a meeting invite.
    7. Propose next steps (demo, discovery call) and attempt to schedule or collect availability.
    8. Close politely and confirm follow-up actions.

    Required data to collect (verify with prospect):
    - lead_name (full name)
    - company (organization)
    - title (role)
    - email (confirm by repeating)
    - phone (confirm by repeating)
    - location / time zone
    - primary_pain_points (list)
    - current_solution (if any)
    - budget_estimate (free-text or range)
    - decision_timeline (e.g., "3 months")
    - decision_maker_confirmed (yes/no)
    - interest_level (low/medium/high)
    - meeting_scheduled (yes/no)
    - meeting_time (ISO 8601 or human-readable), if scheduled

    End-of-call outputs (must produce these exactly when call is complete):
    1) Human-readable call_summary: 2–4 short paragraphs summarizing the conversation and next steps.
    2) lead_record JSON object with the fields listed above plus:
       - source: "voice_call"
       - notes: free-text highlights
       - recommended_next_step (e.g., "Send demo invite", "Schedule discovery with AE")
       - timestamp: call end ISO 8601 time
    Return the JSON as a single machine-readable JSON object (no surrounding commentary) and ensure all collected fields appear (use empty string or null where unknown).

    Safety and compliance:
    - If the prospect asks for pricing specifics outside published ranges, provide only approved price ranges or refer to sales for exact quotes.
    - If the prospect requests escalation, flag decision_maker_confirmed and recommend immediate handoff to an Account Executive.
    - If the prospect refuses to provide contact info, still produce a summary with available details and set contact fields to empty.

    Failure handling:
    - If any required field is uncertain, ask a clarifying question in the call.
    - If unable to reach the prospect or if they hang up prematurely, produce a short summary indicating the status and any partial data captured.

    Keep interactions efficient: aim to qualify and capture the lead within a typical SDR call (5–10 minutes).""",
        )

    @function_tool
    async def get_faq_info(self, query: str = "all"):
        """
            Tool: FAQ Information Retriever

            Purpose:
            - Retrieve company information, product details, pricing, and frequently asked questions from the preloaded FAQ data.

            Parameters:
            - query (str): The type of information to retrieve. Options:
                - "all": Return all FAQ data
                - "company": Return company basic information
                - "products": Return product information
                - "pricing": Return pricing information
                - "faq": Return FAQ questions and answers
                - Any specific field name from the FAQ data

            Behavior and constraints:
            - Access the preloaded FAQ data from the assistant's memory.
            - Return relevant information based on the query parameter.
            - If no data is available, return an appropriate message.

            Usage:
            - Use this tool whenever you need to answer questions about the company, products, pricing, or services.
            - Call this tool before answering company-related questions to ensure accurate information.
            """
        if not self.faq_data:
            return "No FAQ data available. Please ensure the FAQ file is loaded."
        
        query_lower = query.lower()
        
        if query_lower == "all":
            return json.dumps(self.faq_data, indent=2)
        elif query_lower == "company":
            company_info = {
                "company": self.faq_data.get("company"),
                "industry": self.faq_data.get("industry"),
                "headquarters": self.faq_data.get("headquarters"),
                "founders": self.faq_data.get("founders"),
                "founded": self.faq_data.get("founded"),
                "description": self.faq_data.get("description")
            }
            return json.dumps(company_info, indent=2)
        elif query_lower == "products":
            return json.dumps(self.faq_data.get("products", []), indent=2)
        elif query_lower == "pricing":
            return json.dumps(self.faq_data.get("pricing", {}), indent=2)
        elif query_lower == "faq":
            return json.dumps(self.faq_data.get("faq", {}), indent=2)
        elif query_lower in self.faq_data:
            return json.dumps(self.faq_data.get(query_lower), indent=2)
        else:
            # Try to find the key in the FAQ data
            for key, value in self.faq_data.items():
                if query_lower in key.lower():
                    return json.dumps({key: value}, indent=2)
            return f"No information found for query: {query}. Available sections: company, products, pricing, faq"

    @function_tool
    async def record_lead(self, lead_record: dict):
        """
            Tool: Lead Recorder

            Purpose:
            - Persist a structured lead record into the local data/leads.json store. This tool should be called when the assistant has gathered sufficient information to create a lead.

            Parameters:
            - lead_record: A dictionary containing lead information with the following fields:
                - lead_name (str): Full name of the lead.
                - company (str): Organization name.
                - title (str): Role or job title.
                - email (str): Contact email (confirm by repeating).
                - phone (str): Contact phone number (confirm by repeating).
                - location (str): Location or time zone.
                - primary_pain_points (list): List of identified pain points.
                - current_solution (str): Current solution in use, if any.
                - budget_estimate (str): Free-text or range of budget estimate.
                - decision_timeline (str): Expected decision timeline (e.g., "3 months").
                - decision_maker_confirmed (str): "yes" or "no".
                - interest_level (str): "low", "medium", or "high".
                - meeting_scheduled (str): "yes" or "no".
                - meeting_time (str): ISO 8601 or human-readable meeting time, if scheduled.
                - source (str): Source of the lead, e.g., "voice_call".
                - notes (str): Free-text highlights from the conversation.
                - recommended_next_step (str): Suggested next step, e.g., "Send demo invite".
                - timestamp (str): Call end ISO 8601 time.

            Behavior and constraints:
            - Append the provided lead record to data/leads.json, creating the file if it does not exist.
            - Ensure all required fields are present; use empty strings or nulls for unknown values.
            - Return a short status string indicating success or failure.

            Usage:
            - Use this tool only to record structured lead information after qualification.
            """
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_dir, "data", "leads.json")

        # Load or initialize file
        data = []
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    content = f.read().strip()
                    if content:
                        data = json.loads(content)
            except Exception as e:
                logger.error(f"Error reading leads file: {e}")
        
        with open(file_path, 'w') as f:
            data.append(lead_record)
            json.dump(data, f, indent=2)
            return "Lead record saved successfully."
    
    @function_tool
    async def get_summary(self):
        """
            Tool: Call Summary Creator & Saver

            Behavior:
            - Read the latest entry from data/call_summaries.json.
            - Create a very short (1-sentence) lead-facing summary.
            - Persist a broader summary into data/summary.json with a timestamp.
            - Return the short summary string.
        """
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        call_summaries_path = os.path.join(base_dir, "data", "call_summaries.json")
        summary_path = os.path.join(base_dir, "data", "summary.json")

        small_summary = "No call summary available."
        broad_summary = ""

        try:
            # Read the latest call summary if available
            if os.path.exists(call_summaries_path):
                with open(call_summaries_path, "r") as f:
                    content = f.read().strip()
                    if content:
                        data = json.loads(content)
                        if data:
                            latest = data[-1]
                            if isinstance(latest, dict):
                                # Prefer explicit fields commonly used
                                broad_summary = (
                                    latest.get("call_summary")
                                    or latest.get("summary")
                                    or latest.get("assistant_summary")
                                    or latest.get("transcript")
                                    or json.dumps(latest, ensure_ascii=False)
                                )
                            else:
                                broad_summary = str(latest)

            # Create a short, lead-facing summary: first meaningful sentence or truncated text
            if broad_summary:
                sentences = re.split(r'(?<=[\.\!\?])\s+', broad_summary.strip())
                if sentences and sentences[0].strip():
                    small_summary = sentences[0].strip()
                else:
                    txt = broad_summary.strip()
                    small_summary = (txt[:160] + "...") if len(txt) > 160 else txt
            else:
                small_summary = "No call summary available."

            # Ensure output directory exists and write the broad summary with timestamp
            try:
                os.makedirs(os.path.dirname(summary_path), exist_ok=True)
                out = {
                    "broad_summary": broad_summary if broad_summary else "",
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                }
                with open(summary_path, "w") as sf:
                    json.dump(out, sf, indent=2, ensure_ascii=False)
            except Exception as e:
                logger.error(f"Error writing summary.json: {e}")

            return small_summary

        except Exception as e:
            logger.error(f"Error retrieving/creating call summary: {e}")
            return "Error retrieving call summary."

def prewarm(proc: JobProcess):
    # preload VAD (recommended)
    proc.userdata["vad"] = silero.VAD.load()

    # preload FAQ JSON
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        faq_path = os.path.join(base_dir, "data", "faq.json")

        if os.path.exists(faq_path):
            with open(faq_path, "r") as f:
                data = json.load(f)
                proc.userdata["faq"] = data
                logger.info(f"Loaded {len(data)} FAQ entries.")
        else:
            proc.userdata["faq"] = {}
            logger.warning("faq.json not found.")
    except Exception as e:
        logger.error(f"Error preloading faq.json: {e}")
        proc.userdata["faq"] = {}



async def entrypoint(ctx: JobContext):
    # Logging setup
    # Add any other context you want in all log entries here
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    # Set up a voice AI pipeline using OpenAI, Cartesia, AssemblyAI, and the LiveKit turn detector
    session = AgentSession(
        # Speech-to-text (STT) is your agent's ears, turning the user's speech into text that the LLM can understand
        # See all available models at https://docs.livekit.io/agents/models/stt/
        stt=deepgram.STT(model="nova-3"),
        # A Large Language Model (LLM) is your agent's brain, processing user input and generating a response
        # See all available models at https://docs.livekit.io/agents/models/llm/
        llm=google.LLM(
                model="gemini-2.5-flash",
            ),
        # Text-to-speech (TTS) is your agent's voice, turning the LLM's text into speech that the user can hear
        # See all available models as well as voice selections at https://docs.livekit.io/agents/models/tts/
        tts=murf.TTS(
                voice="en-UK-hazel", 
                style="Conversation",
                tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
                text_pacing=True
            ),
        # VAD and turn detection are used to determine when the user is speaking and when the agent should respond
        # See more at https://docs.livekit.io/agents/build/turns
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        # allow the LLM to generate a response while waiting for the end of turn
        # See more at https://docs.livekit.io/agents/build/audio/#preemptive-generation
        preemptive_generation=True,
    )

    # To use a realtime model instead of a voice pipeline, use the following session setup instead.
    # (Note: This is for the OpenAI Realtime API. For other providers, see https://docs.livekit.io/agents/models/realtime/))
    # 1. Install livekit-agents[openai]
    # 2. Set OPENAI_API_KEY in .env.local
    # 3. Add `from livekit.plugins import openai` to the top of this file
    # 4. Use the following session setup instead of the version above
    # session = AgentSession(
    #     llm=openai.realtime.RealtimeModel(voice="marin")
    # )

    # Metrics collection, to measure pipeline performance
    # For more information, see https://docs.livekit.io/agents/build/metrics/
    usage_collector = metrics.UsageCollector()

    @session.on("metrics_collected")
    def _on_metrics_collected(ev: MetricsCollectedEvent):
        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)

    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage: {summary}")

    ctx.add_shutdown_callback(log_usage)

    # Retrieve FAQ data from prewarmed data
    faq_data = ctx.proc.userdata.get("faq", {})
    logger.info(f"Starting session with FAQ data: {len(faq_data)} items loaded")

    # # Add a virtual avatar to the session, if desired
    # # For other providers, see https://docs.livekit.io/agents/models/avatar/
    # avatar = hedra.AvatarSession(
    #   avatar_id="...",  # See https://docs.livekit.io/agents/models/avatar/plugins/hedra
    # )
    # # Start the avatar and wait for it to join
    # await avatar.start(session, room=ctx.room)

    # Start the session, which initializes the voice pipeline and warms up the models
    await session.start(
        agent=Assistant(faq_data=faq_data),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            # For telephony applications, use `BVCTelephony` for best results
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    # Join the room and connect to the user
    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
