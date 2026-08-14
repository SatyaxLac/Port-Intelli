import unittest
from unittest.mock import Mock, patch

import pandas as pd

from backend.data.price_fetcher import fetch_yfinance_price


class PriceFetcherTests(unittest.TestCase):
    @patch("backend.data.price_fetcher.yf.Ticker")
    def test_fetch_yfinance_price_uses_fast_info_first(self, ticker_mock):
        ticker = Mock()
        ticker.fast_info = {"lastPrice": 123.45}
        ticker_mock.return_value = ticker

        self.assertEqual(fetch_yfinance_price("TATAMOTORS"), 123.45)
        ticker_mock.assert_called_once_with("TATAMOTORS.NS")
        ticker.history.assert_not_called()

    @patch("backend.data.price_fetcher.yf.Ticker")
    def test_fetch_yfinance_price_falls_back_to_history(self, ticker_mock):
        ticker = Mock()
        ticker.fast_info = {}
        ticker.history.return_value = pd.DataFrame({"Close": [100.0, 108.25]})
        ticker_mock.return_value = ticker

        self.assertEqual(fetch_yfinance_price("DRREDDY"), 108.25)

    @patch("backend.data.price_fetcher.yf.Ticker")
    def test_fetch_yfinance_price_falls_back_to_info(self, ticker_mock):
        ticker = Mock()
        ticker.fast_info = {}
        ticker.history.return_value = pd.DataFrame()
        ticker.info = {"regularMarketPrice": "77.7"}
        ticker_mock.return_value = ticker

        self.assertEqual(fetch_yfinance_price("FEDERALBNK"), 77.7)

    @patch("backend.data.price_fetcher.yf.Ticker")
    def test_fetch_yfinance_price_returns_none_without_price(self, ticker_mock):
        ticker = Mock()
        ticker.fast_info = {}
        ticker.history.return_value = pd.DataFrame()
        ticker.info = {}
        ticker_mock.return_value = ticker

        self.assertIsNone(fetch_yfinance_price("FEDERALBNK"))

    @patch("backend.data.price_fetcher.yf.Ticker")
    def test_fetch_yfinance_price_falls_back_to_last_price_attr(self, ticker_mock):
        # Simulates a FastInfo object where the dict-key "lastPrice" is absent
        # (e.g. pre-market) but the attribute last_price still carries the value.
        fast_info = Mock(spec=[])  # no .get() so we use a spec-less Mock with manual attrs
        fast_info.get = Mock(return_value=None)  # dict-like .get("lastPrice") misses
        fast_info.last_price = 88.5
        ticker = Mock()
        ticker.fast_info = fast_info
        ticker_mock.return_value = ticker

        self.assertEqual(fetch_yfinance_price("TATAMOTORS"), 88.5)
        ticker.history.assert_not_called()

    @patch("backend.data.price_fetcher.yf.Ticker", side_effect=RuntimeError("network down"))
    def test_fetch_yfinance_price_returns_none_on_error(self, _ticker_mock):
        self.assertIsNone(fetch_yfinance_price("TATAMOTORS"))


if __name__ == "__main__":
    unittest.main()
