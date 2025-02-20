# tests/test_app.py
import unittest
import json
from app import app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_create_and_get_user(self):
        # Create user
        response = self.client.post(
            "/users",
            json={"name": "Jane Doe", "email": "jane@example.com"}
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        user_id = data["id"]

        # Fetch user
        response = self.client.get(f"/users/{user_id}")
        self.assertEqual(response.status_code, 200)
        user_data = json.loads(response.data)
        self.assertEqual(user_data["name"], "Jane Doe")

    # Add tests for other CRUD operations as needed


if __name__ == "__main__":
    unittest.main()
