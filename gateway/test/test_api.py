"""
Verify behavior of the API
"""
import json
import os
import time

from flask_testing import TestCase

from app.api import API


class APITest(TestCase):

    def create_app(self):
        self.api = API(port=os.getenv("MARKET_GATEWAY_PORT", "15000"),
                       products_service_host=os.getenv('PRODUCT_SERVICE_HOST'),
                       carts_service_host=os.getenv('CART_SERVICE_HOST'),
                       cashier_service_host=os.getenv('CASHIER_SERVICE_HOST'))
        app = self.api.api
        app.config['TESTING'] = True
        return app

    def setUp(self):
        self.client = self.api.api.test_client()

        def health_check():
            # health check
            for _ in range(3):
                r = self.client.get('/health-check')
                if r.status_code == 200:
                    return
                time.sleep(5)
            assert False, 'Services never became ready'

        health_check()

    def test_get_product(self):
        r = self.client.get('/products')
        assert r.status_code == 200, 'Expected 200 for GET /products but got {0}'.format(r.status_code)
        assert 'products' in r.json, 'Expected "products" in data, but got {0}'.format(r.json)
        assert type(r.json['products']) == list, 'Expected "products" to be a list, but got {0}'.format(
            type(r.json['products']))

    def test_get_cart(self):
        """Verify correct creation and retrieval of a cart"""
        r = self.client.post('/carts')
        assert r.status_code == 201
        assert 'cart' in r.json, 'Expected "cart" in json, but got {0}'.format(r.json)
        assert 'id' in r.json['cart'], 'Expected "id" in "cart" of json, but got {0}'.format(r.json['cart'])
        assert 'items' in r.json['cart'], 'Expected "items" in "cart" of json, but got {0}'.format(r.json['cart'])
        r = self.client.get('/cart/'+r.json['cart']['id'])
        assert r.status_code == 200
        assert 'cart' in r.json, 'Expected "cart" in json, but got {0}'.format(r.json)
        assert 'id' in r.json['cart'], 'Expected "id" in "cart" of json, but got {0}'.format(r.json['cart'])
        assert 'items' in r.json['cart'], 'Expected "items" in "cart" of json, but got {0}'.format(r.json['cart'])

    def test_create_with_items(self):
        """Verify successful addition of items upon cart creation"""
        r = self.client.post('/carts')
        assert r.status_code == 201
        assert 'cart' in r.json, 'Expected "cart" in json, but got {0}'.format(r.json)
        assert 'id' in r.json['cart'], 'Expected "id" in "cart" of json, but got {0}'.format(r.json['cart'])
        assert 'items' in r.json['cart'], 'Expected "items" in "cart" of json, but got {0}'.format(r.json['cart'])

    def test_update_items(self):
        """Verify successful addition and removal of products to the cart"""
        r = self.client.post('/carts')
        assert r.status_code == 201
        r = self.client.post('/cart/' + r.json['cart']['id'], data=json.dumps({
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
        assert len([x for x in r.json['cart']['items'] if x == 'AP1']) == 3
        assert len([x for x in r.json['cart']['items'] if x == 'CH1']) == 1
        # Verify accurate calculation of cart invoice
        r = self.client.get('/cart/' + r.json['cart']['id'] + '/invoice')
        assert r.status_code == 200
        assert 'invoice' in r.json
        assert 'total' in r.json['invoice']
        assert 'items' in r.json['invoice']
