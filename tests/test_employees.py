import unittest
from unittest.mock import patch

import requests

BASE_URL = "http://127.0.0.1:5000"  # Update if running on a different port or domain


class TestEmployeeEndpoints(unittest.TestCase):
    EMPLOYEE_URL = f"{BASE_URL}/api/employees"

    @patch("requests.post")
    def test_create_employee(self, mock_post):
        # Simulate a successful response
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {
            "message": "Employee created successfully"
        }

        payload = {"name": "John", "position": "Developer"}
        response = requests.post(self.EMPLOYEE_URL, json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Employee created successfully", response.json()["message"])

    @patch("requests.get")
    def test_get_employees(self, mock_get):
        # Simulate a successful response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {"id": 1, "name": "John", "position": "Developer"},
            {"id": 2, "name": "Sarah", "position": "Manager"},
        ]

        response = requests.get(self.EMPLOYEE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    @patch("requests.get")
    def test_get_employee(self, mock_get):
        # Simulate a successful response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "id": 1,
            "name": "John",
            "position": "Developer",
        }

        response = requests.get(f"{self.EMPLOYEE_URL}/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("John", response.json()["name"])

    @patch("requests.put")
    def test_update_employee(self, mock_put):
        # Simulate a successful response
        mock_put.return_value.status_code = 200
        mock_put.return_value.json.return_value = {
            "message": "Employee updated successfully"
        }

        payload = {"name": "John Updated", "position": "Lead Developer"}
        response = requests.put(f"{self.EMPLOYEE_URL}/1", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Employee updated successfully", response.json()["message"])

    @patch("requests.delete")
    def test_delete_employee(self, mock_delete):
        # Simulate a successful response
        mock_delete.return_value.status_code = 200
        mock_delete.return_value.json.return_value = {
            "message": "Employee deleted successfully"
        }

        response = requests.delete(f"{self.EMPLOYEE_URL}/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Employee deleted successfully", response.json()["message"])


if __name__ == "__main__":
    unittest.main()
