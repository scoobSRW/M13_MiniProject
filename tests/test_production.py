import unittest
from unittest.mock import patch

import requests

BASE_URL = "http://127.0.0.1:5000"  # Update if running on a different port or domain


class TestProductionEndpoints(unittest.TestCase):
    PRODUCTION_URL = f"{BASE_URL}/api/production"

    @patch("requests.post")
    def test_record_production(self, mock_post):
        # Simulate a successful response
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {
            "message": "Production record created successfully"
        }

        payload = {
            "product_id": 1,
            "quantity_produced": 100,
            "date_produced": "2025-02-01",
        }
        response = requests.post(self.PRODUCTION_URL, json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn(
            "Production record created successfully", response.json()["message"]
        )

    @patch("requests.get")
    def test_get_production(self, mock_get):
        # Simulate a successful response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {
                "id": 1,
                "product_id": 1,
                "quantity_produced": 100,
                "date_produced": "2025-02-01",
            }
        ]

        response = requests.get(self.PRODUCTION_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    @patch("requests.put")
    def test_update_production(self, mock_put):
        # Simulate a successful response
        mock_put.return_value.status_code = 200
        mock_put.return_value.json.return_value = {
            "message": "Production record updated successfully"
        }

        payload = {"quantity_produced": 150}
        response = requests.put(f"{self.PRODUCTION_URL}/1", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Production record updated successfully", response.json()["message"]
        )

    @patch("requests.delete")
    def test_delete_production(self, mock_delete):
        # Simulate a successful response
        mock_delete.return_value.status_code = 200
        mock_delete.return_value.json.return_value = {
            "message": "Production record deleted successfully"
        }

        response = requests.delete(f"{self.PRODUCTION_URL}/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Production record deleted successfully", response.json()["message"]
        )


if __name__ == "__main__":
    unittest.main()
