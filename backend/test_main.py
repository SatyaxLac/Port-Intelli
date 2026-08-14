import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.main import _get_cors_origins, app


class ApiRouteTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("backend.main.answer_query", return_value="Portfolio answer")
    def test_ask_trims_question_before_answering(self, answer_query_mock):
        response = self.client.post("/ask", json={"question": "  How is TATAMOTORS?  "})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"response": "Portfolio answer"})
        answer_query_mock.assert_called_once_with("How is TATAMOTORS?")

    @patch("backend.main.answer_query")
    def test_ask_rejects_empty_question(self, answer_query_mock):
        response = self.client.post("/ask", json={"question": "   "})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Question must not be empty."})
        answer_query_mock.assert_not_called()

    def test_cors_allows_local_frontend_origin(self):
        response = self.client.options(
            "/ask",
            headers={
                "Origin": "http://localhost:8080",
                "Access-Control-Request-Method": "POST",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get("access-control-allow-origin"), "http://localhost:8080")
        self.assertNotIn("access-control-allow-credentials", response.headers)

    @patch.dict("os.environ", {"CORS_ALLOW_ORIGINS": " https://app.example.com, http://localhost:3000 "})
    def test_cors_origins_can_be_configured_from_env(self):
        self.assertEqual(
            _get_cors_origins(),
            ["https://app.example.com", "http://localhost:3000"],
        )


if __name__ == "__main__":
    unittest.main()
