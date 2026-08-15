import json
import os
from typing import Any, Dict, List

from dotenv import load_dotenv

load_dotenv()

DEFAULT_HOLDINGS = [
    # Large-cap IT
    {"symbol": "TCS", "quantity": 15, "avg_price": 3500.0},
    {"symbol": "INFY", "quantity": 40, "avg_price": 1500.0},
    {"symbol": "HCLTECH", "quantity": 30, "avg_price": 1400.0},
    {"symbol": "WIPRO", "quantity": 80, "avg_price": 450.0},
    {"symbol": "TECHM", "quantity": 25, "avg_price": 1250.0},
    # Banks & Financial
    {"symbol": "HDFCBANK", "quantity": 35, "avg_price": 1600.0},
    {"symbol": "ICICIBANK", "quantity": 50, "avg_price": 950.0},
    {"symbol": "SBIN", "quantity": 60, "avg_price": 600.0},
    {"symbol": "KOTAKBANK", "quantity": 20, "avg_price": 1750.0},
    {"symbol": "AXISBANK", "quantity": 40, "avg_price": 1050.0},
    {"symbol": "INDUSINDBK", "quantity": 30, "avg_price": 1400.0},
    {"symbol": "FEDERALBNK", "quantity": 100, "avg_price": 140.0},
    {"symbol": "BAJFINANCE", "quantity": 10, "avg_price": 6800.0},
    {"symbol": "BAJAJFINSV", "quantity": 20, "avg_price": 1550.0},
    {"symbol": "HDFCLIFE", "quantity": 50, "avg_price": 600.0},
    {"symbol": "SBILIFE", "quantity": 25, "avg_price": 1400.0},
    # Energy & Oil
    {"symbol": "RELIANCE", "quantity": 20, "avg_price": 2500.0},
    {"symbol": "ONGC", "quantity": 100, "avg_price": 250.0},
    {"symbol": "BPCL", "quantity": 60, "avg_price": 550.0},
    {"symbol": "NTPC", "quantity": 80, "avg_price": 350.0},
    {"symbol": "POWERGRID", "quantity": 90, "avg_price": 280.0},
    {"symbol": "COALINDIA", "quantity": 70, "avg_price": 400.0},
    # Auto
    {"symbol": "TATAMOTORS", "quantity": 50, "avg_price": 620.0},
    {"symbol": "MARUTI", "quantity": 5, "avg_price": 10500.0},
    {"symbol": "EICHERMOT", "quantity": 10, "avg_price": 3800.0},
    {"symbol": "HEROMOTOCO", "quantity": 12, "avg_price": 4200.0},
    {"symbol": "BAJAJ-AUTO", "quantity": 8, "avg_price": 8500.0},
    {"symbol": "M&M", "quantity": 25, "avg_price": 1500.0},
    # Pharma & Healthcare
    {"symbol": "SUNPHARMA", "quantity": 35, "avg_price": 1200.0},
    {"symbol": "DRREDDY", "quantity": 10, "avg_price": 4500.0},
    {"symbol": "CIPLA", "quantity": 30, "avg_price": 1200.0},
    {"symbol": "DIVISLAB", "quantity": 8, "avg_price": 3500.0},
    {"symbol": "APOLLOHOSP", "quantity": 6, "avg_price": 5500.0},
    # FMCG & Consumer
    {"symbol": "HINDUNILVR", "quantity": 18, "avg_price": 2400.0},
    {"symbol": "ITC", "quantity": 100, "avg_price": 440.0},
    {"symbol": "NESTLEIND", "quantity": 3, "avg_price": 22000.0},
    {"symbol": "BRITANNIA", "quantity": 10, "avg_price": 5000.0},
    {"symbol": "DABUR", "quantity": 60, "avg_price": 550.0},
    {"symbol": "TATACONSUM", "quantity": 30, "avg_price": 900.0},
    # Infrastructure & Materials
    {"symbol": "LT", "quantity": 15, "avg_price": 3400.0},
    {"symbol": "ULTRACEMCO", "quantity": 5, "avg_price": 8500.0},
    {"symbol": "GRASIM", "quantity": 15, "avg_price": 2200.0},
    {"symbol": "JSWSTEEL", "quantity": 40, "avg_price": 800.0},
    {"symbol": "TATASTEEL", "quantity": 100, "avg_price": 140.0},
    {"symbol": "ADANIENT", "quantity": 15, "avg_price": 2400.0},
    {"symbol": "ADANIPORTS", "quantity": 30, "avg_price": 1200.0},
    # Telecom
    {"symbol": "BHARTIARTL", "quantity": 25, "avg_price": 1400.0},
    # Specialty
    {"symbol": "TITAN", "quantity": 12, "avg_price": 3200.0},
    {"symbol": "ASIANPAINT", "quantity": 15, "avg_price": 2800.0},
    {"symbol": "PIDILITIND", "quantity": 12, "avg_price": 2700.0},
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
