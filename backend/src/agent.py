import logging
import os

from dotenv import load_dotenv
from livekit.agents import JobContext, JobProcess, WorkerOptions, cli

# IMPORTANT: Import plugins here at module level to register them on the main thread
# before any worker threads are created. This prevents "Plugins must be registered on the main thread" errors.
from livekit.plugins import silero, murf, google, deepgram, noise_cancellation
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("agent")

# Configure logger to ensure it's visible
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(name)-15s %(message)s',
    datefmt='%H:%M:%S'
)

load_dotenv(".env")

def prewarm(proc: JobProcess):
    """Route prewarm to appropriate day agent."""
    # Plugins are already imported at module level, so they're registered on main thread
    # Now we can safely import and call day-specific prewarm functions
    log_msg = "Loading Day 4 Agent..."
    logger.info(log_msg)
    print(f"🔵 {log_msg}")
    try:
        from tutor_agent import prewarm as day4_prewarm
    except ImportError:
        from tutor_agent import prewarm as day4_prewarm
    day4_prewarm(proc, silero)

async def entrypoint(ctx: JobContext):
    """Route entrypoint to appropriate day agent."""
    log_msg = "Starting Day 4 Agent..."
    logger.info(log_msg)
    print(f"🔵 {log_msg}")
    try:
        from tutor_agent import entrypoint as day4_entrypoint
    except ImportError:
        from tutor_agent import entrypoint as day4_entrypoint
    await day4_entrypoint(ctx)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))