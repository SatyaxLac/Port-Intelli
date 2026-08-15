import os
import time
from typing import Any, Dict, List, Optional

from google import genai
from dotenv import load_dotenv

load_dotenv()

# Simple in-memory cache: { symbol: (timestamp, summary) }
_SUMMARY_CACHE: Dict[str, tuple[float, str]] = {}
_CACHE_TTL_SECONDS = 600  # 10 minutes

_client: Optional[genai.Client] = None


def _get_client() -> Optional[genai.Client]:
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            _client = genai.Client(
                api_key=api_key,
                http_options={"timeout": 10_000},
            )
    return _client


def summarize_news(symbol: str, articles: List[Dict[str, Any]]) -> str:
    """Summarize recent news for a stock symbol using Gemini with 10-minute caching."""
    if not articles:
        return f"No recent news found for {symbol}."

    now = time.time()
    if symbol in _SUMMARY_CACHE:
        cached_time, cached_summary = _SUMMARY_CACHE[symbol]
        if now - cached_time < _CACHE_TTL_SECONDS:
            return cached_summary

    client = _get_client()
    if not client:
        # Fallback summary from headline if Gemini API key is unavailable
        first_title = articles[0].get("title", "")
        return f"Recent headline for {symbol}: '{first_title}'"

    content = "\n\n".join([f"Title: {a.get('title', '')}\nSummary: {a.get('summary', '')}" for a in articles[:3]])

    prompt = (
        f"You are a financial reasoning assistant. Based on the recent news for {symbol}, "
        f"summarize in 1-2 sentences why the stock may have gone up or down recently. "
        f"Be concise, factual, and include any macro/geopolitical reasons if mentioned.\n\n"
        f"News Articles:\n{content}\n\n"
        f"Answer:"
    )

    try:
        response = client.models.generate_content(model="gemini-flash-latest", contents=prompt)
        summary = response.text.strip()
        _SUMMARY_CACHE[symbol] = (now, summary)
        return summary
    except Exception as e:
        print(f"[ERROR] Gemini summarization failed for {symbol}: {e}")
        first_title = articles[0].get("title", "")
        return f"Recent news updates suggest market movement based on: {first_title}"
