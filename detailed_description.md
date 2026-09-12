# SellMate AI — Detailed Description

## Overview
SellMate AI is a beginner-to-intermediate Python project that simulates a smart assistant for e-commerce sellers. It runs as a single-file Streamlit web app and answers questions about selling on major marketplaces, while also handling practical calculations sellers need every day — like profit and profit margin. The project intentionally avoids paid AI APIs (like OpenAI) so it can run for free, fully offline in terms of AI logic, using only rule-based Python code.

## Purpose
The goal is to give new sellers (or anyone learning Python/Streamlit) a working example of:
- How a simple chatbot can be built without machine learning or external APIs
- How to structure conversational logic and multi-step conversations
- How to build small, practical calculators wrapped in a chat interface
- How to organize business logic (calculations, intent detection) separately from the UI layer (Streamlit)

## How It Works
1. **User Input** — The user types a message or clicks a quick-action button in the Streamlit chat interface.
2. **Intent Detection** — The `detect_intent()` function scans the message for keywords (case-insensitive) to classify it into categories such as `greeting`, `profit_calculation`, `amazon`, `product_sourcing`, etc.
3. **Response Handling** — Based on the detected intent, `get_response()` either:
   - Returns a canned answer from the knowledge base (e.g., "What is Shopify?")
   - Starts or continues a multi-step conversation (e.g., the profit calculator, which asks one question at a time)
   - Instantly parses and calculates a "quick" command like `profit 40 15 4 7 2`
   - Falls back to a polite "not sure what you mean" message for unrecognized input
4. **Chat Interface** — Streamlit displays the conversation history and renders the bot's replies in a chat-style UI.

## Core Features
- **Knowledge Base**: Built-in facts about Amazon, Walmart, eBay, Shopify, product research, sourcing, listings, and hiring a virtual assistant.
- **Intent Detection**: Lightweight keyword matching (no ML model required) that recognizes greetings, goodbyes, help requests, and marketplace/topic questions.
- **Profit Calculator**:
  - Step-by-step mode: the bot asks for selling price, product cost, shipping, marketplace fees, and other costs one at a time.
  - Quick mode: users can type all five numbers directly in one message (e.g., `profit 40 15 4 7 2`) for an instant result.
  - Formula used: `Profit = Selling Price − Product Cost − Shipping − Fees − Other Costs`, and `Margin % = (Profit / Selling Price) × 100`.
- **Error Handling**: Gracefully manages empty input, non-numeric input, and negative values without crashing.
- **Quick-Action Buttons**: One-click shortcuts in the UI for common tasks (Calculate Profit, Product Research, Product Sourcing, Marketplace Help).
- **Session Memory**: Conversation history and in-progress multi-step flows (like the profit calculator) are preserved during the browser session using Streamlit's `session_state`.

## Technology Stack
- **Python 3.11+** — core programming language
- **Streamlit** — web-based chat interface
- **Python standard library (`re`)** — text pattern matching for intent detection and number extraction

## Architecture
The code is organized into clear logical sections within a single file, mirroring good separation of concerns even without multiple files:
1. Knowledge base data
2. Intent detection logic
3. Profit calculation utilities
4. Response generation (including multi-step conversation handling)
5. Streamlit UI layer

This makes it easy to later split into multiple files (`chatbot.py`, `intent_detector.py`, `utilities.py`, `app.py`, etc.) or extend with a real machine-learning intent classifier (TF-IDF + Logistic Regression) without rewriting the core logic.

## Limitations (Current Version)
- No real machine-learning model — intent detection is purely keyword-based.
- No persistent storage — chat history resets when the browser session ends.
- No integration with real marketplace APIs (Amazon, Walmart, eBay, Shopify) — all information is static/educational.

## Possible Future Improvements
- Add a TF-IDF + Logistic Regression intent classifier with a confidence threshold
- Connect to real marketplace APIs for live product/pricing data
- Add a database for saving profit calculations and chat history
- Add user accounts and login
- Add voice input/output
- Expand the knowledge base with more detailed marketplace guidance
