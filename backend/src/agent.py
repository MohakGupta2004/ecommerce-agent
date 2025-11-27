
import logging, json, os
from dotenv import load_dotenv
from datetime import datetime
from livekit.agents import (
    Agent, AgentSession, JobContext, JobProcess,
    MetricsCollectedEvent, RoomInputOptions, WorkerOptions,
    cli, metrics, tokenize, function_tool
)
from livekit.plugins import murf, silero, google, deepgram, noise_cancellation
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("FoodGroceriesAgent")
load_dotenv(".env")

# ----------------------------------
# 📦 LOAD CATALOG (FOOD + GROCERIES + RECIPES)
# ----------------------------------
def load_catalog():
    with open("src/data/catalog.json", "r") as f:
        return json.load(f)

# ----------------------------------
# 💾 SAVE ORDER INTO JSON FILE
# ----------------------------------
def save_order(order_obj):
    file_path = "src/data/orders.json"
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump([], f)

    with open(file_path, "r") as f:
        orders = json.load(f)

    orders.append(order_obj)
    with open(file_path, "w") as f:
        json.dump(orders, f, indent=4)

# ----------------------------------
# 🤖 FOOD + GROCERY AGENT
# ----------------------------------
class GroceryFoodAgent(Agent):
    def __init__(self, catalog):
        self.foods = catalog["foods"]
        self.groceries = catalog["groceries"]
        self.recipes = catalog["recipes"]

        self.cart = []
        self.customer_name = None

        # Create a readable item list
        display_menu = ", ".join(f'{i["name"]} (₹{i["price"]})' for i in self.foods)
        display_groceries = ", ".join(f'{i["name"]} (₹{i["price"]})' for i in self.groceries)

        super().__init__(instructions=f"""
        You are a friendly Food + Grocery Voice Assistant from Crave.

        🍽 Available Foods: {display_menu}
        🛒 Grocery Items: {display_groceries}

        📌 Rules:
        - Ask user's name first. When they tell you their name, IMMEDIATELY call set_customer_name() with their name.
        - Identify if the user wants FOOD or wants to COOK something.
        - If user says a dish name from recipes, suggest its ingredients from groceries.
        - When user chooses something, call add_to_cart().
        - When user says "done", call finalize_order().
        - Confirm each step politely.
        """)

    # --------------------------
    # 👤 Set Customer Name Tool
    # --------------------------
    @function_tool
    async def set_customer_name(self, name: str):
        """
        Sets the customer's name when they introduce themselves.
        """
        self.customer_name = name
        return f"Nice to meet you {name}! What would you like today?"

    # --------------------------
    # 🔍 Search Functions
    # --------------------------
    def search_food(self, name):
        for f in self.foods:
            if name.lower() in f["name"].lower():
                return f
        return None

    def search_grocery(self, name):
        for g in self.groceries:
            if name.lower() in g["name"].lower():
                return g
        return None

    # --------------------------
    # 🛒 Add to Cart Tool
    # --------------------------
    @function_tool
    async def add_to_cart(self, item: str):
        """
        Adds food or grocery to cart.
        """
        found = self.search_food(item) or self.search_grocery(item)
        if found:
            self.cart.append(found)
            return f"Added {found['name']} to your cart!"
        return "Item not found!"

    # --------------------------
    # 🧾 Finalize and Save Order
    # --------------------------
    @function_tool
    async def finalize_order(self):
        """
        Saves order to JSON.
        """
        total = sum(i["price"] for i in self.cart)
        order = {
            "customer": self.customer_name,
            "items": self.cart,
            "total": total,
            "timestamp": datetime.now().isoformat()
        }
        save_order(order)
        return f"Order confirmed for {self.customer_name}! Total = ₹{total}"

# ----------------------------------
# 🚀 LIVEKIT ENTRYPOINT
# ----------------------------------
def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()

async def entrypoint(ctx: JobContext):
    catalog = load_catalog()

    session = AgentSession(
        stt=deepgram.STT(model="nova-3"),
        llm=google.LLM(model="gemini-2.5-flash"),
        tts=murf.TTS(
            voice="en-UK-hazel",
            style="Conversation",
            tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2)
        ),
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        preemptive_generation=True,
    )

    usage_collector = metrics.UsageCollector()
    @session.on("metrics_collected")
    def _metrics(ev: MetricsCollectedEvent):
        usage_collector.collect(ev.metrics)

    await session.start(
        agent=GroceryFoodAgent(catalog),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        )
    )

    # 👋 Startup Greeting
    session.generate_reply(
        instructions="You are a friendly assistant. Greet the user and ask their name."
    )

    await ctx.connect()

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
