import unittest
import requests

BASE_URL = "http://127.0.0.1:5000"  # Update if running on a different port or domain

class TestProductionEndpoints(unittest.TestCase):
    PRODUCTION_URL = f"{BASE_URL}/api/production"

    def test_record_production(self):
        payload = {"product_id": 1, "quantity_produced": 100, "date_produced": "2023-12-25"}
        response = requests.post(self.PRODUCTION_URL, json=payload)
        self.assertEqual(response.status_code, 201)

    def test_get_production(self):
        response = requests.get(self.PRODUCTION_URL)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
