import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
import requests
from app import create_app
from config import DevelopmentConfig

BASE_URL = "http://127.0.0.1:5000"  # Update if running on a different port or domain

class TestEmployeeEndpoints(unittest.TestCase):
    EMPLOYEE_URL = f"{BASE_URL}/api/employees"

    @classmethod
    def setUpClass(cls):
        """Set up a test app context."""
        cls.app = create_app(DevelopmentConfig)
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        """Remove the test app context."""
        cls.app_context.pop()

    @patch("app.models.models.Employee.query")
    def test_get_employees(self, mock_query):
        mock_query.all.return_value = [
            MagicMock(id=1, name="John Doe", position="Manager"),
            MagicMock(id=2, name="Jane Smith", position="Developer"),
        ]

        response = requests.get(self.EMPLOYEE_URL)
        self.assertEqual(response.status_code, 200)

    def test_create_employee(self):
        payload = {"name": "John Doe", "position": "Manager"}
        response = requests.post(self.EMPLOYEE_URL, json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Employee created successfully", response.json().get("message"))

if __name__ == "__main__":
    unittest.main()
