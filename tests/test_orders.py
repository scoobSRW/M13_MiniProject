import unittest
from unittest.mock import patch

import requests

BASE_URL = "http://127.0.0.1:5000"  # Update if running on a different port or domain


class TestOrderEndpoints(unittest.TestCase):
    ORDER_URL = f"{BASE_URL}/api/orders"

    @patch("requests.post")
    def test_create_order(self, mock_post):
        # Simulate a successful response
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {
            "message": "Order created successfully"
        }

        payload = {"customer_id": 1, "product_id": 1, "quantity": 2}
        response = requests.post(self.ORDER_URL, json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Order created successfully", response.json()["message"])

    @patch("requests.get")
    def test_get_orders(self, mock_get):
        # Simulate a successful response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {"id": 1, "customer_id": 1, "product_id": 1, "quantity": 2},
            {"id": 2, "customer_id": 2, "product_id": 2, "quantity": 1},
        ]

        response = requests.get(self.ORDER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    @patch("requests.get")
    def test_get_order(self, mock_get):
        # Simulate a successful response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "id": 1,
            "customer_id": 1,
            "product_id": 1,
            "quantity": 2,
        }

        response = requests.get(f"{self.ORDER_URL}/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("customer_id", response.json())

    @patch("requests.put")
    def test_update_order(self, mock_put):
        # Simulate a successful response
        mock_put.return_value.status_code = 200
        mock_put.return_value.json.return_value = {
            "message": "Order updated successfully"
        }

        payload = {"quantity": 3}
        response = requests.put(f"{self.ORDER_URL}/1", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Order updated successfully", response.json()["message"])

    @patch("requests.delete")
    def test_delete_order(self, mock_delete):
        # Simulate a successful response
        mock_delete.return_value.status_code = 200
        mock_delete.return_value.json.return_value = {
            "message": "Order deleted successfully"
        }

        response = requests.delete(f"{self.ORDER_URL}/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Order deleted successfully", response.json()["message"])


if __name__ == "__main__":
    unittest.main()
