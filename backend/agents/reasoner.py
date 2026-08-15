# backend/agents/reasoner.py

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, Optional
from backend.portfolio.holdings import get_holdings
from backend.data.price_fetcher import fetch_yfinance_price
from backend.data.news_fetcher import fetch_news
from backend.agents.gemini_summarizer import summarize_news

def _process_stock(stock: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Process price, news, and AI insights for a single stock holding."""
    symbol = stock["symbol"]
    qty = stock["quantity"]
    avg_price = stock["avg_price"]

    current_price = fetch_yfinance_price(symbol)
    
    # If live price fails (e.g. delisted or temporary API error), fallback to avg_price
    # so the stock doesn't disappear from the user's dashboard entirely.
    if current_price is None:
        current_price = avg_price

    invested = avg_price * qty
    current_value = current_price * qty
    gain = current_value - invested

    news = fetch_news(symbol)
    insight = summarize_news(symbol, news)

    return {
        "symbol": symbol,
        "quantity": qty,
        "avg_price": avg_price,
        "current_price": current_price,
        "invested": invested,
        "current_value": current_value,
        "gain": gain,
        "insight": insight
    }

def analyze_portfolio_data() -> Dict[str, Any]:
    """Fetch, analyze, and return aggregated portfolio statistics and stock insights."""
    holdings = get_holdings()

    stocks = []
    total_invested = 0.0
    total_current = 0.0

    # Parallelize stock data enrichment using thread pool
    max_workers = min(len(holdings), 5) if holdings else 1
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_stock = {executor.submit(_process_stock, h): h for h in holdings}
        for future in as_completed(future_to_stock):
            try:
                stock_data = future.result()
                if stock_data:
                    stocks.append(stock_data)
                    total_invested += stock_data["invested"]
                    total_current += stock_data["current_value"]
            except Exception as e:
                holding = future_to_stock[future]
                print(f"[ERROR] Failed to analyze stock {holding.get('symbol')}: {e}")

    # Maintain consistent stock order if desired
    stocks.sort(key=lambda s: s["symbol"])

    return {
        "total_invested": total_invested,
        "total_current": total_current,
        "net_gain": total_current - total_invested,
        "stocks": stocks
    }
