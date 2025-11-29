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

logger = logging.getLogger("ShoppingAgent")
load_dotenv(".env")

# ----------------------------------
# 📦 LOAD PRODUCTS CATALOG
# ----------------------------------
def load_catalog():
    with open("src/data/products.json", "r") as f:
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
# 🛍️ SHOPPING AGENT
# ----------------------------------
class ShoppingAgent(Agent):
    def __init__(self, products):
        self.products = products
        self.last_listed_products = []

        super().__init__(instructions="""
        You are a friendly voice shopping assistant. You help customers browse and buy products.

        📌 Rules:
        - ALWAYS use list_products() to search the catalog. NEVER invent or guess products.
        - When user asks to browse (e.g., "show me hoodies", "blue items", "mugs under 500"), call list_products() with appropriate filters.
        - Support natural follow-up queries like "show me cheaper ones" or "what about red?"
        - When user wants to buy something (e.g., "I'll take that", "buy the second one", "order two of those"), use create_order() with the correct product_id and quantity.
        - Use simple, conversational English. Keep responses brief and natural for voice.
        - If user refers to "the first one", "the last hoodie", "that blue mug", resolve it from the last listed products.
        - After placing an order, confirm the order ID and total.
        - If user asks about their last order, call get_last_order().
        """)

    # --------------------------
    # � List Products Tool
    # --------------------------
    @function_tool
    async def list_products(
        self,
        category: str = "",
        color: str = "",
        max_price: int = 0,
        search: str = ""
    ):
        """
        Browse and filter products by category, color, max price, or text search.
        Returns matching products from the catalog.
        
        Args:
            category: Filter by category (e.g., 'clothing', 'electronics', 'home')
            color: Filter by color (e.g., 'blue', 'black', 'red')
            max_price: Maximum price filter (e.g., 500, 1000)
            search: Text search in product name or description
        """
        results = self.products

        # Apply filters
        if category:
            results = [p for p in results if p.get("category", "").lower() == category.lower()]
        
        if color:
            results = [p for p in results if p.get("color", "").lower() == color.lower()]
        
        if max_price > 0:
            results = [p for p in results if p.get("price", 0) <= max_price]
        
        if search:
            search_lower = search.lower()
            results = [
                p for p in results
                if search_lower in p.get("name", "").lower() or search_lower in p.get("description", "").lower()
            ]

        # Store results for reference resolution
        self.last_listed_products = results

        if not results:
            return "No products found matching your criteria."

        # Format results for voice
        formatted = []
        for idx, p in enumerate(results, 1):
            formatted.append(f"{idx}. {p['name']} - ₹{p['price']} ({p.get('color', 'N/A')})")
        
        return "\n".join(formatted)

    # --------------------------
    # 🛒 Create Order Tool
    # --------------------------
    @function_tool
    async def create_order(self, line_items: list[dict]):
        """
        Place an order with one or more products.
        
        Args:
            line_items: List of items, each with 'product_id' and 'quantity'
                       Example: [{"product_id": "prod_001", "quantity": 2}]
        """
        if not line_items:
            return "No items provided for the order."

        order_items = []
        total = 0

        for item in line_items:
            product_id = item.get("product_id")
            quantity = item.get("quantity", 1)

            # Find product
            product = next((p for p in self.products if p["id"] == product_id), None)
            
            if not product:
                return f"Product {product_id} not found."

            item_total = product["price"] * quantity
            total += item_total

            order_items.append({
                "product_id": product_id,
                "name": product["name"],
                "price": product["price"],
                "quantity": quantity,
                "item_total": item_total
            })

        # Generate order
        order_id = f"ORD_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        order = {
            "order_id": order_id,
            "items": order_items,
            "total": total,
            "timestamp": datetime.now().isoformat()
        }

        save_order(order)
        
        return f"Order {order_id} placed successfully! Total: ₹{total}. You ordered {len(order_items)} item(s)."

    # --------------------------
    # 📦 Get Last Order Tool
    # --------------------------
    @function_tool
    async def get_last_order(self):
        """
        Retrieve the most recent order from orders.json.
        """
        file_path = "src/data/orders.json"
        
        if not os.path.exists(file_path):
            return "No orders found."

        with open(file_path, "r") as f:
            orders = json.load(f)

        if not orders:
            return "No orders found."

        last_order = orders[-1]
        
        items_summary = ", ".join([f"{item['name']} (x{item['quantity']})" for item in last_order["items"]])
        
        return f"Order {last_order['order_id']}: {items_summary}. Total: ₹{last_order['total']}"

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
        agent=ShoppingAgent(catalog),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        )
    )

    # 👋 Startup Greeting
    session.generate_reply(
        instructions="You are a friendly shopping assistant. Greet the user and ask how you can help them today."
    )

    await ctx.connect()

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
