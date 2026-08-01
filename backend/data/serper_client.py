import os
from typing import Any, Dict, List, Optional

import requests
from dotenv import load_dotenv

load_dotenv()

SERPER_NEWS_URL = "https://google.serper.dev/news"

def _format_news_item(item: Dict[str, Any]) -> Dict[str, str]:
    return {
        "title": item.get("title", "No title"),
        "summary": item.get("snippet", ""),
        "url": item.get("link", ""),
    }

def search_news(
    query: str,
    num_results: int = 3,
    api_key: Optional[str] = None,
    raise_on_error: bool = False,
) -> List[Dict[str, Any]]:
    serper_key = api_key or os.getenv("SERPER_API_KEY")
    headers = {
        "X-API-KEY": serper_key or "",
        "Content-Type": "application/json",
    }
    data = {"q": query, "num": num_results}

    try:
        response = requests.post(SERPER_NEWS_URL, headers=headers, json=data, timeout=5)
        response.raise_for_status()
        items = response.json().get("news", [])
        return [_format_news_item(item) for item in items]
    except Exception as e:
        if raise_on_error:
            raise
        print(f"[ERROR] Serper failed: {e}")
        return []
