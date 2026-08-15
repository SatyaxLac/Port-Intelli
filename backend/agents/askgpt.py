import os
import re
from typing import Any, Dict, Optional
from google import genai
from backend.agents.reasoner import analyze_portfolio_data
from backend.data.news_fetcher import fetch_news
from backend.data.price_fetcher import fetch_yfinance_price
from backend.portfolio.holdings import get_holdings
from dotenv import load_dotenv

load_dotenv()

_client: Optional[genai.Client] = None

def _get_client() -> Optional[genai.Client]:
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            _client = genai.Client(api_key=api_key, http_options={"timeout": 15000})
    return _client

def answer_query(question: str, portfolio: Optional[Dict[str, Any]] = None) -> str:
    """Answer user natural language questions about portfolio stocks using Gemini."""
    if portfolio is None:
        portfolio = analyze_portfolio_data()

    # 1. Try matching a stock symbol in the question from our holdings
    target_symbol = None
    all_holdings = get_holdings()
    for holding in all_holdings:
        symbol = holding["symbol"]
        pattern = rf"\b{re.escape(symbol)}\b"
        if re.search(pattern, question, re.IGNORECASE):
            target_symbol = symbol
            break
            
    # 2. If no holding matches, see if they mentioned a stock ticker in ALL CAPS (e.g. INFY, ZOMATO)
    if not target_symbol:
        words = re.findall(r'\b[A-Z]{3,10}\b', question)
        if words:
            target_symbol = words[0]
            
    # 3. If they just said the name (like 'dabur'), we can try a simple lower/upper match heuristic
    if not target_symbol:
        for word in question.split():
            if len(word) >= 3 and word.isalpha():
                # Checking if the uppercased word is a known holding symbol
                for holding in all_holdings:
                    if word.upper() == holding["symbol"]:
                        target_symbol = holding["symbol"]
                        break

    # Fetch live context for the target symbol
    context = ""
    if target_symbol:
        try:
            price = fetch_yfinance_price(target_symbol)
            news = fetch_news(target_symbol)
            news_text = "\n".join([f"- {n.get('title')}" for n in news[:3]])
            context = f"Live Data for {target_symbol}:\nCurrent Price: {price} INR\nRecent News:\n{news_text}\n\n"
        except Exception as e:
            print(f"[ERROR] Could not fetch live data for {target_symbol}: {e}")

    # Stringify portfolio for context
    port_summary = []
    for s in portfolio.get("stocks", []):
        sym = s.get("symbol", "?")
        qty = s.get("quantity", 0)
        avg = s.get("avg_price", 0) or 0
        cur = s.get("current_price", 0) or 0
        gain = s.get("gain", 0) or 0
        port_summary.append(f"{sym}: {qty} shares, Avg: {avg:.2f}, Current: {cur:.2f}, Gain: {gain:.2f}")
    
    port_text = "\n".join(port_summary)
    
    total_val = portfolio.get("total_current", 0) or 0
    total_gain = portfolio.get("net_gain", 0) or 0

    prompt = f"""You are a helpful and knowledgeable AI financial portfolio assistant.
The user is asking a question about their portfolio or the stock market.
You must answer their question directly based on their portfolio data and any live market data provided.
Do NOT just summarize the news unless asked to. Answer their exact query (e.g. if they ask for a price, give the price).

User's Portfolio Overview (Total Value: {total_val:.2f}, Total Gain: {total_gain:.2f}):
{port_text}

{context}
User's Question: {question}

Answer directly and concisely:"""

    client = _get_client()
    if not client:
        return "Error: Gemini API key is not configured."
        
    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"[ERROR] AskGPT generation failed: {e}")
        return "I'm sorry, I couldn't generate an answer right now. Please try again later."
