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
        "keywords": ["amazon", "fba", "amazon seller", "fbm"],
        "response": (
            "**Amazon** is the world's largest e-commerce marketplace, with two main "
            "ways to sell:\n\n"
            "1. **FBA (Fulfillment by Amazon)** — you ship your inventory to Amazon's "
            "warehouses; they handle storage, packing, shipping, and customer service. "
            "Easier to scale, but you pay storage + fulfillment fees.\n"
            "2. **FBM (Fulfillment by Merchant)** — you store and ship orders yourself. "
            "Lower fees, but more hands-on work.\n\n"
            "**Getting started:** create a Seller Central account (Individual or "
            "Professional plan), choose a category, list your product with a "
            "keyword-rich title and images, then decide FBA vs FBM.\n\n"
            "**Typical costs:** referral fee (~8–15% of sale price depending on "
            "category), plus FBA fulfillment fees if you use that option.\n\n"
            "**Good for:** sellers who want the biggest possible customer base and "
            "don't mind competing on price and reviews."
        ),
    },
    "walmart": {
        "keywords": ["walmart", "walmart seller", "walmart marketplace"],
        "response": (
            "**Walmart Marketplace** lets third-party sellers list products on "
            "Walmart.com alongside Walmart's own inventory.\n\n"
            "**How it's different from Amazon:**\n"
            "- Application/approval process is more selective — you apply and Walmart "
            "reviews your business before you can sell.\n"
            "- Referral fees are often similar to or slightly lower than Amazon's, "
            "depending on category.\n"
            "- Less competition than Amazon in many categories, since fewer sellers "
            "are approved.\n"
            "- Walmart Fulfillment Services (WFS) offers Amazon-FBA-style storage and "
            "shipping if you don't want to fulfill orders yourself.\n\n"
            "**Getting started:** apply at marketplace.walmart.com, provide business "
            "details (tax ID, business type), and once approved, list products through "
            "Seller Center.\n\n"
            "**Good for:** established sellers with a track record who want a lower-"
            "competition alternative to Amazon."
        ),
    },
    "ebay": {
        "keywords": ["ebay", "ebay seller", "ebay listing"],
        "response": (
            "**eBay** is one of the oldest online marketplaces, supporting both "
            "auction-style and fixed-price ('Buy It Now') listings.\n\n"
            "**Best suited for:**\n"
            "- Used, refurbished, or collectible items\n"
            "- Niche or hard-to-find products\n"
            "- Sellers testing a product before committing to Amazon/Walmart\n\n"
            "**How it works:** create a seller account, list an item with photos and "
            "a description, choose auction or fixed price, and pay a final value fee "
            "(typically ~10–13% of the sale, varies by category) when it sells.\n\n"
            "**Tips for success:** build seller feedback/ratings early with small "
            "sales, price competitively by checking 'Sold' listings for similar items, "
            "and offer fast shipping with tracking to boost your seller rating."
        ),
    },
    "shopify": {
        "keywords": ["shopify", "my own store", "online store", "build a website"],
        "response": (
            "**Shopify** lets you build your own branded online store instead of "
            "selling on someone else's marketplace.\n\n"
            "**Pros:**\n"
            "- Full control over branding, pricing, and the customer experience\n"
            "- You own customer data (email lists, buying history) — great for "
            "repeat business\n"
            "- No marketplace referral fees (though Shopify has monthly + payment "
            "processing fees)\n\n"
            "**Cons:**\n"
            "- You're responsible for driving your own traffic (ads, SEO, social "
            "media) — there's no built-in customer base like Amazon has\n"
            "- More setup work: choosing a theme, apps, and payment gateway\n\n"
            "**Getting started:** sign up for a plan, pick a theme, add products, "
            "connect a payment processor (like Shopify Payments or Stripe), and set "
            "up shipping rates.\n\n"
            "**Good for:** sellers building a long-term brand, or those who already "
            "have an audience (social media, email list) to drive traffic."
        ),
    },
    "product_research": {
        "keywords": ["research", "find a product", "profitable product", "what should i sell",
                     "product idea", "niche"],
        "response": (
            "**Product research** is about finding items worth selling. Here's a "
            "practical process:\n\n"
            "**1. Look for the right criteria:**\n"
            "- Steady, year-round demand (avoid pure seasonal fads unless that's your strategy)\n"
            "- Low-to-moderate competition (check how many reviews top listings have)\n"
            "- Sells for roughly $15–$50 (cheap enough to buy impulsively, expensive "
            "enough for decent profit margin)\n"
            "- Small and lightweight (keeps shipping/storage costs down)\n"
            "- Not fragile, not electronic/battery-restricted, not a legal minefield "
            "(no trademarked characters, no safety-regulated items unless you know what you're doing)\n\n"
            "**2. Where to look for ideas:**\n"
            "- Amazon Best Sellers and Movers & Shakers pages\n"
            "- Google Trends (check if interest is rising or falling over time)\n"
            "- Social media (TikTok, Pinterest, Instagram) for emerging trends\n"
            "- Marketplace research tools: Jungle Scout, Helium 10, Keepa (for Amazon "
            "price/sales history)\n\n"
            "**3. Validate the idea before committing:**\n"
            "- Check estimated monthly sales of similar listings\n"
            "- Read negative reviews on competing products — that's your chance to "
            "make a better version\n"
            "- Run the numbers through a profit calculator (try 'calculate my profit' "
            "here) before ordering inventory\n\n"
            "**Rule of thumb:** the best products solve a small, specific frustration "
            "better than what's currently available — not just 'a cheaper version' of "
            "something popular."
        ),
    },
    "product_sourcing": {
        "keywords": ["sourcing", "supplier", "manufacturer", "wholesale", "dropship",
                     "dropshipping", "alibaba"],
        "response": (
            "**Product sourcing** means finding a reliable supplier to make or supply "
            "your product. Here are the main routes:\n\n"
            "**1. Overseas manufacturing (e.g. Alibaba, Global Sources)**\n"
            "- Lowest per-unit cost, good for scaling\n"
            "- Requires ordering samples first, negotiating MOQ (minimum order "
            "quantity), and longer shipping times (weeks, not days)\n"
            "- Watch for red flags: suppliers with no verified reviews, prices that "
            "seem too good to be true, or refusal to provide samples\n\n"
            "**2. Domestic wholesalers/distributors**\n"
            "- Faster shipping, easier communication, smaller MOQs\n"
            "- Higher per-unit cost than overseas manufacturing\n\n"
            "**3. Dropshipping**\n"
            "- No upfront inventory cost — the supplier ships directly to your "
            "customer when you make a sale\n"
            "- Lower profit margins and less control over shipping times/quality\n"
            "- Good for testing product ideas with minimal risk before committing to "
            "bulk inventory\n\n"
            "**4. Private label / white label**\n"
            "- You buy a generic product and brand it as your own (custom packaging, "
            "logo)\n"
            "- Common path for building a recognizable brand on Amazon\n\n"
            "**Before committing to any supplier:**\n"
            "- Always order a sample first to check quality\n"
            "- Ask for their business license/certifications if manufacturing "
            "physical goods\n"
            "- Compare quotes from at least 3 suppliers\n"
            "- Clarify payment terms, lead time, and what happens with defective units"
        ),
    },
    "product_listing": {
        "keywords": ["listing", "list a product", "write a listing", "product title"],
        "response": (
            "A strong product listing typically has:\n\n"
            "- **Title:** clear, keyword-rich, includes brand + key feature + size/"
            "quantity if relevant\n"
            "- **Images:** at least 5–7 high-quality photos, including lifestyle shots "
            "and a size-reference image\n"
            "- **Bullet points:** 4–5 bullets highlighting the top benefits (not just "
            "features) — answer 'what does this do for the buyer?'\n"
            "- **Description:** expands on the bullets, answers common questions, and "
            "addresses objections a buyer might have\n"
            "- **Keywords/backend search terms:** include relevant search terms buyers "
            "might use, even if they don't fit naturally in the visible title/description\n\n"
            "**Tip:** look at your top 3 competitors' listings — what are they missing "
            "in their reviews? That's often a gap you can fill in your own listing."
        ),
    },
    "ecommerce_va": {
        "keywords": ["virtual assistant", "va", "hire help"],
        "response": "An E-commerce VA (Virtual Assistant) helps with tasks like listing products, "
                    "customer service, order processing, and research — freeing up your time to grow the business.",
    },
    "marketplace_compare": {
        "keywords": ["which marketplace", "which platform", "best marketplace",
                     "compare marketplace", "marketplace help", "where should i sell"],
        "response": (
            "Here's a quick comparison to help you choose:\n\n"
            "- **Amazon** — biggest built-in audience, most competition, best for "
            "commodity/consumer products\n"
            "- **Walmart** — lower competition than Amazon, but requires seller "
            "approval\n"
            "- **eBay** — great for used/collectible/niche items, or testing new "
            "products with low commitment\n"
            "- **Shopify** — best for building a long-term brand, but you must drive "
            "your own traffic\n\n"
            "**Simple guideline:** if you're just starting out and want the most "
            "customers with the least setup, start on Amazon or eBay. If you already "
            "have an audience or want full brand control, go with Shopify. Ask me "
            "about any one of these by name for more detail."
        ),
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
        col4.button("🏪 Marketplace Help"): "Which marketplace should I sell on?",
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
