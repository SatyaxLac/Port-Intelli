import json
import os
from typing import Any, Dict, List

from dotenv import load_dotenv

load_dotenv()

DEFAULT_HOLDINGS = [
    {"symbol": "TATAMOTORS", "quantity": 50, "avg_price": 620.0, "pnl": 1500.0},
    {"symbol": "DRREDDY", "quantity": 10, "avg_price": 4500.0, "pnl": -800.0},
    {"symbol": "FEDERALBNK", "quantity": 100, "avg_price": 140.0, "pnl": 1200.0},
]


def _normalize_holding(holding: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "symbol": str(holding["symbol"]).upper(),
        "quantity": float(holding["quantity"]),
        "avg_price": float(holding["avg_price"]),
        "pnl": float(holding.get("pnl", 0.0)),
    }


def get_holdings() -> List[Dict[str, Any]]:
    """Load holdings from PORTFOLIO_HOLDINGS_JSON or return sample holdings."""
    holdings_json = os.getenv("PORTFOLIO_HOLDINGS_JSON")
    if not holdings_json:
        return DEFAULT_HOLDINGS

    try:
        holdings = json.loads(holdings_json)
        if not isinstance(holdings, list):
            raise ValueError("PORTFOLIO_HOLDINGS_JSON must be a JSON list")
        return [_normalize_holding(holding) for holding in holdings]
    except Exception as e:
        print(f"[WARN] Holdings config failed ({e}). Returning sample holdings.")
        return DEFAULT_HOLDINGS
