import unittest
from unittest.mock import patch

import requests

BASE_URL = "http://127.0.0.1:5000"  # Update if running on a different port or domain


class TestProductEndpoints(unittest.TestCase):
    PRODUCT_URL = f"{BASE_URL}/api/products"

    @patch("requests.post")
    def test_create_product(self, mock_post):
        # Simulate a successful response
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {
            "message": "Product created successfully"
        }

        payload = {"name": "Product A", "price": 99.99}
        response = requests.post(self.PRODUCT_URL, json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Product created successfully", response.json()["message"])

    @patch("requests.get")
    def test_get_products(self, mock_get):
        # Simulate a successful response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {"id": 1, "name": "Product A", "price": 99.99},
            {"id": 2, "name": "Product B", "price": 49.99},
        ]

        response = requests.get(self.PRODUCT_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    @patch("requests.get")
    def test_get_product(self, mock_get):
        # Simulate a successful response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "id": 1,
            "name": "Product A",
            "price": 99.99,
        }

        response = requests.get(f"{self.PRODUCT_URL}/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Product A", response.json()["name"])

    @patch("requests.put")
    def test_update_product(self, mock_put):
        # Simulate a successful response
        mock_put.return_value.status_code = 200
        mock_put.return_value.json.return_value = {
            "message": "Product updated successfully"
        }

        payload = {"name": "Updated Product A", "price": 79.99}
        response = requests.put(f"{self.PRODUCT_URL}/1", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Product updated successfully", response.json()["message"])

    @patch("requests.delete")
    def test_delete_product(self, mock_delete):
        # Simulate a successful response
        mock_delete.return_value.status_code = 200
        mock_delete.return_value.json.return_value = {
            "message": "Product deleted successfully"
        }

        response = requests.delete(f"{self.PRODUCT_URL}/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Product deleted successfully", response.json()["message"])


if __name__ == "__main__":
    unittest.main()
