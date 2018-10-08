"""
Verify behavior of the API
"""
import json
import os
import time

from flask_testing import TestCase

from app.carts import API
from store.redis_store import Store

# TODO: Better isolation from the other services, but using docker-compose is fine for now


class APITest(TestCase):

    def create_app(self):
        self.api = API(port=os.getenv("MARKET_CARTS_PORT", "15010"),
                       store=Store(host=os.getenv(
                           'CART_STORE_HOST', 'cart-store')))
        app = self.api.api
        app.config['TESTING'] = True
        return app

    def setUp(self):
        self.client = self.api.api.test_client()
        # health check
        for _ in range(3):
            r = self.client.get('/health-check')
            if r.status_code == 200:
                break
            time.sleep(3)

    def tearDown(self):
        pass

    def test_get_cart(self):
        """Verify correct creation and retrieval of a cart"""
        r = self.client.post('/carts', data=json.dumps({
            'items': {
                'AP1': 4,
                'CH1': 2,
            }
        }))
        assert r.status_code == 201
        ap1 = [x for x in r.json['items'] if x == 'AP1']
        ap1_count = len(ap1)
        ch1 = [x for x in r.json['items'] if x == 'CH1']
        ch1_count = len(ch1)
        assert ap1_count == 4, 'Expected 3 AP1, but got {0} - {1}'.format(
            ap1_count, ap1)
        assert ch1_count == 2, 'Expected 1 CH1, but got {0} - {1}'.format(
            ch1_count, ch1)
        r = self.client.get('/cart/' + r.json['id'])
        assert r.status_code == 200

    def test_update_items(self):
        """Verify successful addition of products to the cart"""
        r = self.client.post('/carts')
        assert r.status_code == 201
        r = self.client.post('/cart/' + r.json['id'], data=json.dumps({
            'add': {
                'AP1': 4,
                'CH1': 2,
            },
            'remove': {
                'AP1': 1,
                'CH1': 1,
            }
        }))
        assert r.status_code == 200
        ap1 = [x for x in r.json['items'] if x == 'AP1']
        ap1_count = len(ap1)
        ch1 = [x for x in r.json['items'] if x == 'CH1']
        ch1_count = len(ch1)
        assert ap1_count == 3, 'Expected 3 AP1, but got {0} - {1}'.format(
            ap1_count, ap1)
        assert ch1_count == 1, 'Expected 1 CH1, but got {0} - {1}'.format(
            ch1_count, ch1)
