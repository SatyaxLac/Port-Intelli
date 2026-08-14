import re
from typing import Any, Dict, Optional

from backend.agents.gemini_summarizer import summarize_news
from backend.agents.reasoner import analyze_portfolio_data
from backend.data.news_fetcher import fetch_news


def answer_query(question: str, portfolio: Optional[Dict[str, Any]] = None) -> str:
    """Answer user natural language questions about portfolio stocks using Gemini and market summaries."""
    if portfolio is None:
        portfolio = analyze_portfolio_data()

    stocks = portfolio.get("stocks", [])
    if not stocks:
        return "Your portfolio currently contains no active stock holdings."

    # Try matching a stock symbol in the question using exact word boundaries
    target_symbol = None
    for stock in stocks:
        symbol = stock["symbol"]
        pattern = rf"\b{re.escape(symbol)}\b"
        if re.search(pattern, question, re.IGNORECASE):
            target_symbol = symbol
            break

    if target_symbol:
        news = fetch_news(target_symbol)
        summary = summarize_news(target_symbol, news)
        return f"Here's what I found about {target_symbol}:\n{summary}"

    # If no specific symbol matched, return an overall portfolio summary
    top_gainers = sorted(stocks, key=lambda x: x.get("gain", 0.0), reverse=True)[:2]
    top_losers = sorted(stocks, key=lambda x: x.get("gain", 0.0))[:2]

    gainers_text = ", ".join([f"{s['symbol']} (INR {s['gain']:+.2f})" for s in top_gainers])
    losers_text = ", ".join([f"{s['symbol']} (INR {s['gain']:+.2f})" for s in top_losers])

    return (
        f"Today's top performers: {gainers_text}.\n"
        f"Biggest declines: {losers_text}.\n"
        f"Ask me about any specific stock symbol (e.g. TATAMOTORS, DRREDDY) for more details."
    )
