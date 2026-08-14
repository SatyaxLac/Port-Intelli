import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.main import app


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


if __name__ == "__main__":
    unittest.main()
