import unittest
from unittest.mock import Mock, patch

from backend.data import news_fetcher
from backend.data.serper_client import search_news


class FetchNewsTests(unittest.TestCase):
    def setUp(self):
        news_fetcher._NEWS_CACHE.clear()

    @patch.dict("os.environ", {}, clear=True)
    @patch("backend.data.news_fetcher.search_news")
    def test_fetch_news_returns_empty_without_api_key(self, search_news_mock):
        self.assertEqual(news_fetcher.fetch_news("TATAMOTORS"), [])
        search_news_mock.assert_not_called()

    @patch.dict("os.environ", {"SERPER_API_KEY": "test-key"}, clear=True)
    @patch("backend.data.news_fetcher.search_news")
    def test_fetch_news_delegates_to_serper_client_and_caches_articles(self, search_news_mock):
        articles = [{"title": "Headline", "summary": "Snippet", "url": "https://example.com"}]
        search_news_mock.return_value = articles

        first_result = news_fetcher.fetch_news("TATAMOTORS")
        second_result = news_fetcher.fetch_news("TATAMOTORS")

        self.assertEqual(first_result, articles)
        self.assertEqual(second_result, articles)
        search_news_mock.assert_called_once_with(
            "TATAMOTORS stock news India",
            num_results=3,
            api_key="test-key",
            raise_on_error=True,
        )

    @patch.dict("os.environ", {"SERPER_API_KEY": "test-key"}, clear=True)
    @patch("backend.data.news_fetcher.search_news")
    def test_fetch_news_does_not_cache_failed_requests(self, search_news_mock):
        articles = [{"title": "Recovered", "summary": "", "url": ""}]
        search_news_mock.side_effect = [RuntimeError("network down"), articles]

        self.assertEqual(news_fetcher.fetch_news("DRREDDY"), [])
        self.assertEqual(news_fetcher.fetch_news("DRREDDY"), articles)
        self.assertEqual(search_news_mock.call_count, 2)


class SerperClientTests(unittest.TestCase):
    @patch.dict("os.environ", {}, clear=True)
    @patch("backend.data.serper_client.requests.post")
    def test_search_news_returns_empty_without_api_key(self, post_mock):
        self.assertEqual(search_news("TATAMOTORS stock news India"), [])
        post_mock.assert_not_called()

    @patch.dict("os.environ", {}, clear=True)
    @patch("backend.data.serper_client.requests.post")
    def test_search_news_raises_without_api_key_when_requested(self, post_mock):
        with self.assertRaises(ValueError):
            search_news("TATAMOTORS stock news India", raise_on_error=True)

        post_mock.assert_not_called()

    @patch.dict("os.environ", {"SERPER_API_KEY": "test-key"}, clear=True)
    @patch("backend.data.serper_client.requests.post")
    def test_search_news_maps_serper_response_to_article_contract(self, post_mock):
        response = Mock()
        response.json.return_value = {
            "news": [
                {
                    "title": "Market update",
                    "snippet": "A concise update",
                    "link": "https://example.com/news",
                },
                {},
            ]
        }
        post_mock.return_value = response

        result = search_news("TATAMOTORS stock news India", num_results=2)

        self.assertEqual(
            result,
            [
                {
                    "title": "Market update",
                    "summary": "A concise update",
                    "url": "https://example.com/news",
                },
                {"title": "No title", "summary": "", "url": ""},
            ],
        )
        response.raise_for_status.assert_called_once()
        post_mock.assert_called_once()
        _, kwargs = post_mock.call_args
        self.assertEqual(kwargs["json"], {"q": "TATAMOTORS stock news India", "num": 2})
        self.assertEqual(kwargs["headers"]["X-API-KEY"], "test-key")
        self.assertEqual(kwargs["timeout"], 5)

    @patch("backend.data.serper_client.requests.post", side_effect=RuntimeError("boom"))
    def test_search_news_preserves_fallback_empty_list_on_error(self, _post_mock):
        self.assertEqual(search_news("query"), [])


if __name__ == "__main__":
    unittest.main()
