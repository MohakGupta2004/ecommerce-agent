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

# Initialize the SQLite database using a context manager, enable WAL and set a busy timeout
conn = sqlite3.connect("users.db")
cursor = conn.cursor()
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS users (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     userName TEXT,
#     securityIdentifier TEXT,
#     cardEnding TEXT,
#     transactionName TEXT,
#     transactionAmount TEXT,
#     transactionLocation TEXT,
#     transactionSource TEXT,
#     transactionTime TEXT,
#     securityQuestion TEXT,
#     securityAnswer TEXT,
#     status TEXT,
#     note TEXT
# )
# """)
# cursor.execute("""
#            insert into users (userName, securityIdentifier, cardEnding, transactionName, transactionAmount, transactionLocation, transactionSource, transactionTime, securityQuestion, securityAnswer, status, note)
#            values ("mohak gupta", "id12345", "6789", "alibaba purchase", "$150.00", "new york, ny", "online", "2024-06-15 14:30:00", "what is your pet's name?", "fluffy", "pending_review", "first time transaction")
#         """)

try:
    cursor.execute("DELETE FROM users WHERE id = ?", (2,))
except sqlite3.OperationalError as e:
    logger.warning("Could not delete initial row: %s", e)

conn.commit()
conn.close()

logger = logging.getLogger("agent")

load_dotenv(".env")


class Assistant(Agent):
    def __init__(self, userName: str = None, securityQuestion: str = None, securityAnswer: str = None):
        self.userName = userName
        self.securityQuestion = securityQuestion
        self.securityAnswer = securityAnswer
        super().__init__(instructions=f"""
 You are a fraud detection assistant from NovaCox bank. You'll call the user when they have any unusual transaction, you need to verify it with them by asking their security question which is {self.securityQuestion}.
    DO NOT ask for any personal information like full card number, CVV, expiry date, etc.
    Before proceeding, confirm the user's identity using their userName: {self.userName}. Only proceed if the user is the right person. Otherwise, terminate the call.
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
        args:
            security_answer (str): The answer provided by the user.
        returns:
            str: Verification result message.
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
    proc.userdata["userName"] = rows[0][1]
    proc.userdata["securityQuestion"] = rows[0][9]
    proc.userdata["securityAnswer"] = rows[0][10]


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
        agent=Assistant(userName=ctx.proc.userdata.get("userName", "Unknown"), securityQuestion=ctx.proc.userdata.get("securityQuestion", "Unknown"), securityAnswer=ctx.proc.userdata.get("securityAnswer", "Unknown")),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            # For telephony applications, use `BVCTelephony` for best results
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )
    session.generate_reply(
        instructions=f"Greet the user with something like this: Hello, this is Sarah from the Fraud Prevention Department at NovaCox Bank. Am I speaking with {ctx.proc.userdata.get('userName', 'Unknown')}?"
    )

    # Join the room and connect to the user
    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
