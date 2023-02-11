import unittest
import sys

sys.path.append('../')
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client() 

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_best_deal(self):
        response = self.client.get('/best-deals/sunglasses')
        json_data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
                list(json_data.keys()), ['amazon', 'flipkart'])
        self.assertEqual(len(json_data['amazon']), 10)
        self.assertEqual(len(json_data['flipkart']), 10)

