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
import sqlite3

conn = sqlite3.connect('users.db')  # Creates a new database file if it doesn’t exist
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
  userName TEXT,
  securityIdentifier TEXT,
  cardEnding TEXT,
  transactionName TEXT,
  transactionAmount TEXT,
  transactionLocation TEXT,
  transactionSource TEXT,
  transactionTime TEXT,
  securityQuestion TEXT,
  securityAnswer TEXT,
  status TEXT,
  note TEXT
)
""")
#cursor.execute("""
#    INSERT INTO users (userName, securityIdentifier, cardEnding, transactionName, transactionAmount, transactionLocation, transactionSource, transactionTime, securityQuestion, securityAnswer, status, note)
#    VALUES ("Mohak Gupta", "ID12345", "6789", "Alibaba purchase", "$150.00", "New York, NY", "Online", "2024-06-15 14:30:00", "What is your pet's name?", "Fluffy", "pending_review", "First time transaction")
#""")

# cursor.execute("DELETE FROM users WHERE userName = 'Mohak Gupta'")

# cursor.execute("SELECT * FROM users")
""" rows = cursor.fetchall()
for row in rows:
    print(row)
 """
conn.commit()
conn.close()


logger = logging.getLogger("agent")

load_dotenv(".env")


class Assistant(Agent):
    def __init__(self, userName: str = None):
        self.userName = userName
        super().__init__(instructions=f"""
 You are a fraud detection assistant from Novatech bank. If someone has any unusual transaction, you need to verify it with them by asking security questions.
    DO NOT ask for any personal information like full card number, CVV, expiry date, etc.
    You have access to a database of users and their recent transactions. Use this information to assist in verifying transactions.
    The database has the following fields:
    - userName
    - securityIdentifier
    - cardEnding
    - transactionName
    - transactionAmount     
    - transactionLocation
    - transactionSource
    - transactionTime
    - securityQuestion
    - securityAnswer
    - status
    - note
    When a user mentions a transaction, look it up in the database using the transactionName, transactionAmount, and cardEnding.
    If the transaction is found and marked as "pending_review", ask the user the corresponding security. If the user answers correctly, mark the transaction as "verified". If the answer is incorrect, mark it as "fraudulent".
        """)

    @function_tool
    async def security_question_lookup(self, security_answer: str) -> str:
        """
        Looks up the security question answer in the database and verifies by asking the user that he's the right person. And the
        user did the transaction or not. 
        """
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT securityAnswer FROM users WHERE userName = ?", (self.userName,))
        row = cursor.fetchone()
        if row and row[0].lower() == security_answer.lower():
            cursor.execute("UPDATE users SET status = 'confirmed_safe' WHERE userName = ?", (self.userName,))
            conn.commit()
            conn.close()
            return "The transaction has been verified successfully."
        else:
            cursor.execute("UPDATE users SET status = 'verification_failed' WHERE userName = ?", (self.userName,))
            conn.commit()
            conn.close()
            return "The answer is incorrect. The transaction has been marked as fraudulent."

    @function_tool
    async def confirm_fraud(self, confirmation: str) -> str:
        """
        Confirms if the user wants to mark the transaction as fraudulent.
        """
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        if confirmation.lower() in ["yes", "y", "confirm", "mark as fraudulent"]:
            cursor.execute("UPDATE users SET status = 'confirmed_fraud' WHERE userName = ?", (self.userName,))
            conn.commit()
            conn.close()
            return "The transaction has been marked as fraudulent."
        else:
            cursor.execute("UPDATE users SET status = 'confirmed_safe' WHERE userName = ?", (self.userName,))
            conn.commit()
            conn.close()
            return "The transaction has been confirmed as safe."

    




def prewarm(proc: JobProcess):
    # preload VAD (recommended)
    proc.userdata["vad"] = silero.VAD.load()

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE status = 'pending_review'")
    rows = cursor.fetchall()
    print(rows[0][0])
    proc.userdata["userName"] = rows[0][0]


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

    # # Add a virtual avatar to the session, if desired
    # # For other providers, see https://docs.livekit.io/agents/models/avatar/
    # avatar = hedra.AvatarSession(
    #   avatar_id="...",  # See https://docs.livekit.io/agents/models/avatar/plugins/hedra
    # )
    # # Start the avatar and wait for it to join
    # await avatar.start(session, room=ctx.room)

    # Start the session, which initializes the voice pipeline and warms up the models
    await session.start(
        agent=Assistant(userName=ctx.proc.userdata.get("userName", "Unknown")),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            # For telephony applications, use `BVCTelephony` for best results
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )
    session.generate_reply(
        instructions=f"Confirm the user's identity: {ctx.proc.userdata.get('userName', 'Unknown')} and only proceed if the user is the right person. Otherwise terminate the call."
    )

    # Join the room and connect to the user
    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
