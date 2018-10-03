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

    def test_get_invoice_api():
        assert False
