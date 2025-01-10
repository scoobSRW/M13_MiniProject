import unittest
import requests

BASE_URL = "http://127.0.0.1:5000"  # Update if running on a different port or domain

class TestUserEndpoints(unittest.TestCase):
    LOGIN_URL = f"{BASE_URL}/users/login"

    def test_login(self):
        payload = {"username": "user1", "password": "adminpassword"}
        response = requests.post(self.LOGIN_URL, json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("auth_token", response.json())

if __name__ == "__main__":
    unittest.main()
