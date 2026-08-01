import os
import time
from typing import List, Dict, Any
from dotenv import load_dotenv
from backend.data.serper_client import search_news

load_dotenv()

# Simple in-memory cache: { symbol: (timestamp, articles) }
_NEWS_CACHE: Dict[str, tuple[float, List[Dict[str, Any]]]] = {}
_CACHE_TTL_SECONDS = 600  # 10 minutes

def fetch_news(symbol: str) -> List[Dict[str, Any]]:
    """Fetch recent news articles for a stock symbol with 10-minute caching."""
    now = time.time()
    if symbol in _NEWS_CACHE:
        cached_time, cached_articles = _NEWS_CACHE[symbol]
        if now - cached_time < _CACHE_TTL_SECONDS:
            return cached_articles

    serper_key = os.getenv("SERPER_API_KEY")
    if not serper_key:
        print(f"[WARN] SERPER_API_KEY not set. Returning empty news for {symbol}.")
        return []

    try:
        articles = search_news(
            f"{symbol} stock news India",
            num_results=3,
            api_key=serper_key,
            raise_on_error=True,
        )
        _NEWS_CACHE[symbol] = (now, articles)
        return articles

    except Exception as e:
        print(f"[ERROR] Serper.dev news fetch failed for {symbol}: {e}")
        return []
