import unittest
import requests

BASE_URL = "http://127.0.0.1:5000"  # Update if running on a different port or domain

class TestOrderEndpoints(unittest.TestCase):
    ORDER_URL = f"{BASE_URL}/api/orders"

    def test_create_order(self):
        payload = {"customer_id": 1, "product_id": 1, "quantity": 2}
        response = requests.post(self.ORDER_URL, json=payload)
        self.assertEqual(response.status_code, 201)

    def test_get_orders(self):
        response = requests.get(self.ORDER_URL)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()