"""
SellMate AI — Your Smart E-commerce Assistant
A single-file, beginner-friendly rule-based chatbot built with Streamlit.

Run with:
    pip install streamlit
    streamlit run sellmate_ai.py
"""

import re
import streamlit as st

# ---------------------------------------------------------------------------
# 1. KNOWLEDGE BASE
# Simple facts the bot can recite. Each topic has keywords (to detect intent)
# and a response (what the bot says).
# ---------------------------------------------------------------------------
KNOWLEDGE_BASE = {
    "amazon": {
        "keywords": ["amazon", "fba", "amazon seller"],
        "response": "Amazon is one of the world's largest e-commerce marketplaces. "
                    "Sellers can list products themselves or use Amazon FBA "
                    "(Fulfillment by Amazon), where Amazon stores, packs, and ships orders for you.",
    },
    "walmart": {
        "keywords": ["walmart", "walmart seller", "walmart marketplace"],
        "response": "Walmart Marketplace lets third-party sellers list products on Walmart.com. "
                    "It has lower seller fees than some competitors but a more selective approval process.",
    },
    "ebay": {
        "keywords": ["ebay", "ebay seller", "ebay listing"],
        "response": "eBay is an auction-and-fixed-price marketplace great for both new and "
                    "used items. It's popular for reselling, collectibles, and niche products.",
    },
    "shopify": {
        "keywords": ["shopify", "my own store", "online store"],
        "response": "Shopify lets you build your own branded online store instead of selling on "
                    "someone else's marketplace. You control pricing, design, and customer data, "
                    "but you're responsible for driving your own traffic.",
    },
    "product_research": {
        "keywords": ["research", "find a product", "profitable product", "what should i sell"],
        "response": "For product research: look for items with steady demand, low competition, "
                    "manageable size/weight, and healthy profit margins. Tools like Jungle Scout, "
                    "Helium 10, or simple bestseller-list browsing can help you spot opportunities.",
    },
    "product_sourcing": {
        "keywords": ["sourcing", "supplier", "manufacturer", "wholesale"],
        "response": "Product sourcing means finding suppliers to make or supply your product. "
                    "Common options: Alibaba (overseas manufacturing), domestic wholesalers, "
                    "or dropshipping suppliers. Always order samples before committing to a supplier.",
    },
    "product_listing": {
        "keywords": ["listing", "list a product", "write a listing", "product title"],
        "response": "A strong product listing has: a clear keyword-rich title, high-quality images, "
                    "bullet points highlighting benefits, and a description that answers buyer questions.",
    },
    "ecommerce_va": {
        "keywords": ["virtual assistant", "va", "hire help"],
        "response": "An E-commerce VA (Virtual Assistant) helps with tasks like listing products, "
                    "customer service, order processing, and research — freeing up your time to grow the business.",
    },
}

# ---------------------------------------------------------------------------
# 2. INTENT DETECTION
# We check the user's message against keyword lists to guess what they want.
# Order matters: more specific checks (like profit calc) go first.
# ---------------------------------------------------------------------------

GREETING_WORDS = ["hi", "hello", "hey", "good morning", "good afternoon"]
GOODBYE_WORDS = ["bye", "goodbye", "see you", "exit", "quit"]
HELP_WORDS = ["help", "what can you do", "options", "menu"]
PROFIT_WORDS = ["profit", "how much will i make", "calculate profit"]
MARGIN_WORDS = ["margin", "profit margin"]


def detect_intent(message: str) -> str:
    """Look at the user's message and return a simple intent label."""
    text = message.lower().strip()

    if not text:
        return "unknown"

    # Quick calculator like "profit 40 15 4 7 2" — numbers present + profit word
    if "profit" in text and re.search(r"\d", text):
        return "quick_profit"

    if any(word in text for word in GREETING_WORDS):
        return "greeting"
    if any(word in text for word in GOODBYE_WORDS):
        return "goodbye"
    if any(word in text for word in HELP_WORDS):
        return "help"
    if any(word in text for word in MARGIN_WORDS):
        return "profit_margin"
    if any(word in text for word in PROFIT_WORDS):
        return "profit_calculation"

    # Check knowledge-base topics
    for topic, data in KNOWLEDGE_BASE.items():
        if any(keyword in text for keyword in data["keywords"]):
            return topic

    return "unknown"


# ---------------------------------------------------------------------------
# 3. PROFIT CALCULATOR
# ---------------------------------------------------------------------------

def calculate_profit(selling_price: float, product_cost: float, shipping: float,
                      fees: float, other_costs: float) -> dict:
    """
    Calculate profit and profit margin.

    Profit = Selling Price - Product Cost - Shipping - Fees - Other Costs
    Profit Margin (%) = (Profit / Selling Price) * 100
    """
    profit = selling_price - product_cost - shipping - fees - other_costs
    margin = (profit / selling_price * 100) if selling_price > 0 else 0.0
    return {"profit": round(profit, 2), "margin": round(margin, 2)}


def parse_quick_profit(text: str):
    """
    Parse a message like 'profit 40 15 4 7 2' into 5 numbers.
    Returns a calculate_profit() result dict, or None if parsing fails.
    """
    numbers = re.findall(r"-?\d+(?:\.\d+)?", text)
    if len(numbers) < 5:
        return None
    try:
        values = [float(n) for n in numbers[:5]]
        if any(v < 0 for v in values):
            return "negative"  # signal for a friendly error message
        return calculate_profit(*values)
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# 4. RESPONSE GENERATION
# Turns an intent into an actual bot reply. Handles the multi-step profit
# conversation using Streamlit's session_state.
# ---------------------------------------------------------------------------

PROFIT_QUESTIONS = [
    ("selling_price", "What is your selling price?"),
    ("product_cost", "What is your product cost?"),
    ("shipping", "What is your shipping cost?"),
    ("fees", "What are your marketplace fees?"),
    ("other_costs", "Any other costs? (enter 0 if none)"),
]


def start_profit_flow():
    """Begin the step-by-step profit calculator conversation."""
    st.session_state.profit_flow = {"step": 0, "answers": {}}
    return PROFIT_QUESTIONS[0][1]


def continue_profit_flow(user_text: str) -> str:
    """Handle one answer in the ongoing profit calculator conversation."""
    flow = st.session_state.profit_flow
    step = flow["step"]
    field_name, _ = PROFIT_QUESTIONS[step]

    try:
        value = float(user_text.strip())
        if value < 0:
            return "That value can't be negative. Please enter a number 0 or higher."
    except ValueError:
        return "That doesn't look like a number. Please enter digits only, e.g. 25.50"

    flow["answers"][field_name] = value
    flow["step"] += 1

    if flow["step"] < len(PROFIT_QUESTIONS):
        return PROFIT_QUESTIONS[flow["step"]][1]

    # All answers collected — calculate and end the flow
    result = calculate_profit(**flow["answers"])
    st.session_state.profit_flow = None
    return (f"✅ Profit: ${result['profit']}\n"
            f"📊 Profit Margin: {result['margin']}%")


def get_response(user_text: str) -> str:
    """Main entry point: turn user text into a bot response."""
    # If we're in the middle of the step-by-step profit flow, keep going
    if st.session_state.get("profit_flow") is not None:
        return continue_profit_flow(user_text)

    intent = detect_intent(user_text)

    if intent == "greeting":
        return ("Hi! I'm SellMate AI. I can help with product research, sourcing, "
                "marketplace questions, and profit calculations. How can I help?")
    if intent == "goodbye":
        return "Goodbye! Come back anytime you need e-commerce help. 👋"
    if intent == "help":
        return ("I can help with:\n"
                "- Amazon, Walmart, eBay, Shopify basics\n"
                "- Product research & sourcing\n"
                "- Product listings\n"
                "- Profit & profit margin calculations\n\n"
                "Try: 'Calculate my profit' or 'profit 40 15 4 7 2'")
    if intent == "profit_calculation":
        return start_profit_flow()
    if intent == "profit_margin":
        return ("Profit margin shows what % of your selling price is profit.\n"
                "Formula: (Profit / Selling Price) × 100\n"
                "Say 'calculate profit' and I'll walk you through it.")
    if intent == "quick_profit":
        result = parse_quick_profit(user_text)
        if result == "negative":
            return "Values can't be negative. Try: profit 40 15 4 7 2"
        if result is None:
            return ("I need 5 numbers: selling price, product cost, shipping, fees, other costs.\n"
                    "Example: profit 40 15 4 7 2")
        return f"✅ Profit: ${result['profit']}\n📊 Profit Margin: {result['margin']}%"
    if intent in KNOWLEDGE_BASE:
        return KNOWLEDGE_BASE[intent]["response"]

    return ("I'm not completely sure what you mean. You can ask me about product "
            "research, sourcing, Amazon, Walmart, eBay, Shopify, or profit calculations.")


# ---------------------------------------------------------------------------
# 5. STREAMLIT UI
# ---------------------------------------------------------------------------

def main():
    st.set_page_config(page_title="SellMate AI", page_icon="🤖")

    st.title("🤖 SellMate AI")
    st.caption("Your Smart E-commerce Assistant")

    with st.sidebar:
        st.header("About SellMate AI")
        st.write("A rule-based assistant for e-commerce sellers: research, "
                 "sourcing, and profit calculations — no paid API needed.")
        st.header("Supported Platforms")
        st.write("• Amazon\n• Walmart\n• eBay\n• Shopify")

    # Set up session state on first run
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "bot", "text": "Hi! I'm SellMate AI. Ask me about product "
                                     "research, sourcing, marketplaces, or profit calculations."}
        ]
    if "profit_flow" not in st.session_state:
        st.session_state.profit_flow = None

    # Quick-action buttons
    col1, col2, col3, col4 = st.columns(4)
    quick_actions = {
        col1.button("💰 Calculate Profit"): "Calculate my profit",
        col2.button("🔎 Product Research"): "How do I find a profitable product?",
        col3.button("📦 Product Sourcing"): "How do I find a supplier?",
        col4.button("🏪 Marketplace Help"): "Tell me about Amazon",
    }
    triggered_text = quick_actions.get(True)

    # Show chat history
    for msg in st.session_state.messages:
        with st.chat_message("assistant" if msg["role"] == "bot" else "user"):
            st.write(msg["text"])

    # Get new input: either typed or from a quick-action button
    user_input = st.chat_input("Type your message...") or triggered_text

    if user_input:
        st.session_state.messages.append({"role": "user", "text": user_input})
        bot_reply = get_response(user_input)
        st.session_state.messages.append({"role": "bot", "text": bot_reply})
        st.rerun()


if __name__ == "__main__":
    main()
