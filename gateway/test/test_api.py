"""
Verify behavior of the API
"""

from flask_testing import TestCase

from app.api import api


class MyTest(TestCase):

    def create_app(self):
        app = api
        app.config['TESTING'] = True
        return app

    def setUp(self):
        self.client = api.test_client()

    def test_get_product(self):
        r = self.client.get('/products')
        assert r.status_code == 200, 'Expected 200 for GET /products but got {0}'.format(r.status_code)

    def test_get_cart(self):
        """Verify correct creation and retrieval of a cart"""
        r = self.client.post('/carts')
        assert r.status_code == 201
        r = self.client.get('/cart/'+r.json['id'])
        assert r.status_code == 200

    def test_update_items(self):
        """Verify successful addition of products to the cart"""
        r = self.client.post('/carts')
        assert r.status_code == 201
        r = self.client.patch('/cart/' + r.json['id'], data={
            'add': {
                'AP1': 4,
                'CH1': 2,
            },
            'remove': {
                'AP1': 1,
                'CH1': 1,
            }
        })
        assert r.status_code == 200
        assert len(x for x in r.json if x == 'AP1') in r.json == 3
        assert len(x for x in r.json if x == 'CH1') in r.json == 1
        # Verify accurate calculation of cart invoice
        r = self.client.get('/cart/' + r.json['id'] + '/invoice')
        assert r.status_code == 200
        # TODO: Assert expected total (need better test isolation)
