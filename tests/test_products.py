import unittest
import requests

BASE_URL = "http://127.0.0.1:5000"  # Update if running on a different port or domain

class TestProductEndpoints(unittest.TestCase):
    PRODUCT_URL = f"{BASE_URL}/api/products"

    def test_get_products(self):
        response = requests.get(self.PRODUCT_URL)
        self.assertEqual(response.status_code, 200)

    def test_create_product(self):
        payload = {"name": "Gadget", "price": 19.99}
        response = requests.post(self.PRODUCT_URL, json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Product created successfully", response.json().get("message"))

if __name__ == "__main__":
    unittest.main()