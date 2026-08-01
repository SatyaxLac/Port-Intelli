import unittest
from unittest.mock import patch

from backend.agents.askgpt import answer_query
from backend.agents.reasoner import analyze_portfolio_data


class ReasonerTests(unittest.TestCase):
    @patch("backend.agents.reasoner.summarize_news")
    @patch("backend.agents.reasoner.fetch_news")
    @patch("backend.agents.reasoner.fetch_yfinance_price")
    @patch("backend.agents.reasoner.get_holdings")
    def test_analyze_portfolio_data_enriches_holdings_and_totals(
        self,
        get_holdings_mock,
        fetch_price_mock,
        fetch_news_mock,
        summarize_news_mock,
    ):
        get_holdings_mock.return_value = [
            {"symbol": "BETA", "quantity": 2, "avg_price": 100.0},
            {"symbol": "ALPHA", "quantity": 3, "avg_price": 50.0},
        ]
        prices = {"BETA": 125.0, "ALPHA": 40.0}
        fetch_price_mock.side_effect = lambda symbol: prices[symbol]
        fetch_news_mock.side_effect = lambda symbol: [{"title": f"{symbol} news"}]
        summarize_news_mock.side_effect = lambda symbol, _articles: f"{symbol} insight"

        portfolio = analyze_portfolio_data()

        self.assertEqual(portfolio["total_invested"], 350.0)
        self.assertEqual(portfolio["total_current"], 370.0)
        self.assertEqual(portfolio["net_gain"], 20.0)
        self.assertEqual([stock["symbol"] for stock in portfolio["stocks"]], ["ALPHA", "BETA"])
        self.assertEqual(portfolio["stocks"][0]["gain"], -30.0)
        self.assertEqual(portfolio["stocks"][1]["gain"], 50.0)

    @patch("backend.agents.reasoner.fetch_yfinance_price", return_value=None)
    @patch("backend.agents.reasoner.get_holdings")
    def test_analyze_portfolio_data_skips_holdings_without_price(self, get_holdings_mock, _price_mock):
        get_holdings_mock.return_value = [
            {"symbol": "MISSING", "quantity": 10, "avg_price": 20.0},
        ]

        portfolio = analyze_portfolio_data()

        self.assertEqual(portfolio["total_invested"], 0.0)
        self.assertEqual(portfolio["total_current"], 0.0)
        self.assertEqual(portfolio["net_gain"], 0.0)
        self.assertEqual(portfolio["stocks"], [])


class AskGptTests(unittest.TestCase):
    @patch("backend.agents.askgpt.summarize_news", return_value="TATAMOTORS moved on recent news.")
    @patch("backend.agents.askgpt.fetch_news", return_value=[{"title": "Tata update"}])
    def test_answer_query_matches_specific_symbol(self, fetch_news_mock, summarize_news_mock):
        portfolio = {
            "stocks": [
                {"symbol": "TATAMOTORS", "gain": 10.0},
                {"symbol": "DRREDDY", "gain": -5.0},
            ]
        }

        response = answer_query("What is happening with TATAMOTORS?", portfolio=portfolio)

        self.assertIn("Here's what I found about TATAMOTORS", response)
        self.assertIn("TATAMOTORS moved on recent news.", response)
        fetch_news_mock.assert_called_once_with("TATAMOTORS")
        summarize_news_mock.assert_called_once()

    def test_answer_query_returns_general_summary_without_symbol(self):
        portfolio = {
            "stocks": [
                {"symbol": "GAINER", "gain": 100.0},
                {"symbol": "FLAT", "gain": 0.0},
                {"symbol": "LOSER", "gain": -50.0},
            ]
        }

        response = answer_query("How is my portfolio doing?", portfolio=portfolio)

        self.assertIn("Today", response)
        self.assertIn("GAINER", response)
        self.assertIn("LOSER", response)

    def test_answer_query_handles_empty_portfolio(self):
        self.assertEqual(
            answer_query("Any update?", portfolio={"stocks": []}),
            "Your portfolio currently contains no active stock holdings.",
        )


if __name__ == "__main__":
    unittest.main()
