import unittest
from unittest.mock import patch

import requests

BASE_URL = "http://127.0.0.1:5000"  # Update if running on a different port or domain


class TestUserEndpoints(unittest.TestCase):
    USER_URL = f"{BASE_URL}/users"

    @patch("requests.post")
    def test_create_user(self, mock_post):
        # Simulate a successful response
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {
            "message": "User created successfully"
        }

        payload = {"username": "newuser", "password": "password123"}
        response = requests.post(self.USER_URL, json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn("User created successfully", response.json()["message"])

    @patch("requests.get")
    def test_get_users(self, mock_get):
        # Simulate a successful response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {"id": 1, "username": "newuser"},
            {"id": 2, "username": "testuser"},
        ]

        response = requests.get(self.USER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    @patch("requests.get")
    def test_get_user(self, mock_get):
        # Simulate a successful response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"id": 1, "username": "newuser"}

        response = requests.get(f"{self.USER_URL}/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("newuser", response.json()["username"])

    @patch("requests.put")
    def test_update_user(self, mock_put):
        # Simulate a successful response
        mock_put.return_value.status_code = 200
        mock_put.return_value.json.return_value = {
            "message": "User updated successfully"
        }

        payload = {"username": "updateduser", "password": "newpassword123"}
        response = requests.put(f"{self.USER_URL}/1", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("User updated successfully", response.json()["message"])

    @patch("requests.delete")
    def test_delete_user(self, mock_delete):
        # Simulate a successful response
        mock_delete.return_value.status_code = 200
        mock_delete.return_value.json.return_value = {
            "message": "User deleted successfully"
        }

        response = requests.delete(f"{self.USER_URL}/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("User deleted successfully", response.json()["message"])


if __name__ == "__main__":
    unittest.main()
