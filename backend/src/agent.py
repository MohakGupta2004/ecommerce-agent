import logging, json, os
from typing import Optional, Annotated
from pydantic import Field
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
# � LOAD ORDERS HISTORY
# ----------------------------------
def load_orders():
    file_path = "src/data/orders.json"
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        return json.load(f)

# ----------------------------------
# 💾 SAVE ORDER INTO JSON FILE
# ----------------------------------
def save_order(order_obj):
    """
    Save order to orders.json. If customer already exists, append to their orders array.
    Otherwise, create a new customer entry.
    
    Structure:
    [
        {
            "customer": "John Doe",
            "orders": [
                {"order_id": "...", "items": [...], "total": ..., "timestamp": "..."},
                {"order_id": "...", "items": [...], "total": ..., "timestamp": "..."}
            ]
        }
    ]
    """
    file_path = "src/data/orders.json"
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump([], f)

    with open(file_path, "r") as f:
        customers = json.load(f)

    customer_name = order_obj.get("customer", "Guest")
    
    # Find existing customer entry
    customer_entry = next((c for c in customers if c.get("customer", "").lower() == customer_name.lower()), None)
    
    # Create order record (without customer field since it's at the parent level)
    order_record = {
        "order_id": order_obj["order_id"],
        "items": order_obj["items"],
        "total": order_obj["total"],
        "timestamp": order_obj["timestamp"]
    }
    
    if customer_entry:
        # Append to existing customer's orders
        customer_entry["orders"].append(order_record)
    else:
        # Create new customer entry
        customers.append({
            "customer": customer_name,
            "orders": [order_record]
        })
    
    with open(file_path, "w") as f:
        json.dump(customers, f, indent=4)

# ----------------------------------
# 🛍️ SHOPPING AGENT
# ----------------------------------
class ShoppingAgent(Agent):
    def __init__(self, products, orders=None):
        self.products = products
        self.orders = orders or []  # Preloaded order history
        self.last_listed_products = []
        self.customer_name = None  # Track current customer

        super().__init__(instructions="""
        You are a friendly voice shopping assistant. You help customers browse and buy products.

        📌 Rules:
        - At the start, greet warmly and ask for the customer's name if you don't know it yet.
        - When customer introduces themselves (e.g., "I'm John", "My name is Sarah"), call set_customer_name() immediately.
        - ALWAYS use list_products() to search the catalog. NEVER invent or guess products.
        - When user asks to browse (e.g., "show me hoodies", "blue items", "mugs under 500"), call list_products() with appropriate filters.
        - Support natural follow-up queries like "show me cheaper ones" or "what about red?"
        - When user wants to buy something, use create_order() with one of these options:
          * Use 'product_name' if user mentions a specific product name (e.g., "Bluetooth Headphones")
          * Use 'position' if user refers to list position (e.g., "the first one", "number 2")
          * Use 'product_id' only if you have the exact ID
        - Use simple, conversational English. Keep responses brief and natural for voice.
        - Use the customer's name in responses to personalize the experience.
        - After placing an order, confirm the order ID and total.
        - If user asks about their previous orders, call get_customer_orders().
        """)

    # --------------------------
    # � List Products Tool
    # --------------------------
    @function_tool
    async def list_products(
        self,
        category: Annotated[Optional[str], Field(default=None)] = None,
        color: Annotated[Optional[str], Field(default=None)] = None,
        max_price: Annotated[Optional[int], Field(default=None)] = None,
        search: Annotated[Optional[str], Field(default=None)] = None
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

        # Apply filters only when explicitly provided
        if category is not None and category:
            results = [p for p in results if p.get("category", "").lower() == category.lower()]
        
        if color is not None and color:
            results = [p for p in results if p.get("color", "").lower() == color.lower()]
        
        if max_price is not None and max_price > 0:
            results = [p for p in results if p.get("price", 0) <= max_price]
        
        if search is not None and search:
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
    # 👤 Set Customer Name Tool
    # --------------------------
    @function_tool
    async def set_customer_name(self, name: str):
        """
        Set or update the customer's name for personalized service.
        
        Args:
            name: Customer's name (e.g., "John", "Sarah")
        """
        self.customer_name = name.strip()
        
        # Check if this is a returning customer
        customer_entry = next((c for c in self.orders if c.get("customer", "").lower() == self.customer_name.lower()), None)
        
        if customer_entry and customer_entry.get("orders"):
            customer_orders = customer_entry["orders"]
            order_count = len(customer_orders)
            last_order = customer_orders[-1]
            last_items = ", ".join([item["name"] for item in last_order.get("items", [])[:2]])
            if len(last_order.get("items", [])) > 2:
                last_items += ", and more"
            
            return f"Welcome back, {self.customer_name}! I see you've ordered with us {order_count} time(s) before. Last time you got {last_items}. How can I help you today?"
        else:
            return f"Great to meet you, {self.customer_name}! How can I help you today?"

    # --------------------------
    # 🛒 Create Order Tool
    # --------------------------
    @function_tool
    async def create_order(self, line_items: list[dict]):
        """
        Place an order with one or more products.
        
        Args:
            line_items: List of items, each with 'product_id' (or 'product_name' or 'position') and 'quantity'
                       Examples: 
                       - [{"product_id": "prod_001", "quantity": 2}]
                       - [{"product_name": "Bluetooth Headphones", "quantity": 1}]
                       - [{"position": 1, "quantity": 1}]  # First item from last search
        """
        if not line_items:
            return "No items provided for the order."

        order_items = []
        total = 0

        for item in line_items:
            product_id = item.get("product_id")
            product_name = item.get("product_name")
            position = item.get("position")
            quantity = item.get("quantity", 1)

            product = None
            
            # Strategy 1: Find by product_id
            if product_id:
                product = next((p for p in self.products if p["id"] == product_id), None)
            
            # Strategy 2: Find by product_name (case-insensitive)
            if not product and product_name:
                product = next(
                    (p for p in self.products if p["name"].lower() == product_name.lower()),
                    None
                )
            
            # Strategy 3: Find by position in last_listed_products
            if not product and position is not None:
                if 1 <= position <= len(self.last_listed_products):
                    product = self.last_listed_products[position - 1]
                else:
                    return f"Position {position} is out of range. Last search had {len(self.last_listed_products)} products."
            
            if not product:
                identifier = product_id or product_name or f"position {position}"
                return f"Product '{identifier}' not found. Please search for products first using list_products()."

            item_total = product["price"] * quantity
            total += item_total

            order_items.append({
                "product_id": product["id"],
                "name": product["name"],
                "price": product["price"],
                "quantity": quantity,
                "item_total": item_total
            })

        # Generate order
        order_id = f"ORD_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        order = {
            "order_id": order_id,
            "customer": self.customer_name or "Guest",
            "items": order_items,
            "total": total,
            "timestamp": datetime.now().isoformat()
        }

        save_order(order)
        
        return f"Order {order_id} placed successfully! Total: ₹{total}. You ordered {len(order_items)} item(s)."

    # --------------------------
    # 📦 Get Customer Orders Tool
    # --------------------------
    @function_tool
    async def get_customer_orders(self):
        """
        Retrieve all orders for the current customer.
        """
        if not self.customer_name:
            return "I don't know your name yet. Please tell me your name first."
        
        file_path = "src/data/orders.json"
        
        if not os.path.exists(file_path):
            return f"No orders found for {self.customer_name}."

        with open(file_path, "r") as f:
            customers = json.load(f)

        # Find customer entry
        customer_entry = next((c for c in customers if c.get("customer", "").lower() == self.customer_name.lower()), None)
        
        if not customer_entry or not customer_entry.get("orders"):
            return f"No previous orders found for {self.customer_name}."
        
        customer_orders = customer_entry["orders"]
        
        # Format order history
        history = []
        for order in customer_orders:
            items_summary = ", ".join([f"{item['name']} (x{item.get('quantity', 1)})" for item in order["items"]])
            history.append(f"Order {order.get('order_id', 'N/A')}: {items_summary} - Total: ₹{order['total']}")
        
        count = len(customer_orders)
        total_spent = sum(o['total'] for o in customer_orders)
        
        return f"{self.customer_name}, you have {count} order(s):\n" + "\n".join(history) + f"\n\nTotal spent: ₹{total_spent}"

# ----------------------------------
# 🚀 LIVEKIT ENTRYPOINT
# ----------------------------------
def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()
    proc.userdata["catalog"] = load_catalog()
    proc.userdata["orders"] = load_orders()

async def entrypoint(ctx: JobContext):
    catalog = ctx.proc.userdata.get("catalog") or load_catalog()
    orders = ctx.proc.userdata.get("orders") or load_orders()

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
        agent=ShoppingAgent(catalog, orders),
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
