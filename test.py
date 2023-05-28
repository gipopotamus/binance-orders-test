import unittest
from order_handler import create_orders
from flask import Flask
import json


class OrderHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_create_orders_with_valid_data(self):
        orders_data = [
            {
                'volume': 100,
                'number': 3,
                'amountDif': 0.5,
                'side': 'BUY',
                'priceMin': 10.0,
                'priceMax': 15.0
            },
            {
                'volume': 200,
                'number': 2,
                'amountDif': 0.3,
                'side': 'SELL',
                'priceMin': 20.0,
                'priceMax': 25.0
            }
        ]
        data = {'orders': orders_data}
        response = self.client.post('/create_orders', data=json.dumps(data), content_type='application/json')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['message'], 'Ордеры успешно созданы')

    def test_create_orders_with_missing_data(self):
        data = {}
        response = self.client.post('/create_orders', data=json.dumps(data), content_type='application/json')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response_data)

    def test_create_orders_with_invalid_order_data(self):
        orders_data = [
            {
                'volume': 100,
                'number': 3,
                'amountDif': 0.5,
                'side': 'BUY',
                'priceMin': 10.0,
                'priceMax': 'invalid'
            }
        ]
        data = {'orders': orders_data}
        response = self.client.post('/create_orders', data=json.dumps(data), content_type='application/json')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response_data)


if __name__ == '__main__':
    unittest.main()
