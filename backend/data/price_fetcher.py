from typing import Optional
import yfinance as yf

def fetch_yfinance_price(symbol: str) -> Optional[float]:
    """Fetch real-time stock price from Yahoo Finance for NSE stocks."""
    try:
        ticker = yf.Ticker(f"{symbol}.NS")
        # Try fast_info first (significantly faster than ticker.info)
        if hasattr(ticker, "fast_info"):
            price = ticker.fast_info.get("lastPrice") or getattr(ticker.fast_info, "last_price", None)
            if price is not None:
                return float(price)

        # Fallback to history
        df = ticker.history(period="1d")
        if not df.empty and "Close" in df.columns:
            return float(df["Close"].iloc[-1])

        # Final fallback to info dict
        price = ticker.info.get("regularMarketPrice")
        return float(price) if price is not None else None
    except Exception as e:
        print(f"[ERROR] Price fetch failed for {symbol}: {e}")
        return None
