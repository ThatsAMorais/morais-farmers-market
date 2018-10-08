"""
Verify behavior of the Products service
"""
import time

from flask_testing import TestCase

from app.products import db, products


class APITest(TestCase):

    def create_app(self):
        app = products
        app.config['TESTING'] = True
        return app

    def setUp(self):
        self.client = products.test_client()
        # health check
        for _ in range(3):
            r = self.client.get('/health-check')
            if r.status_code == 200:
                break
            time.sleep(3)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_products(self):
        for n in range(3):
            i = str(n)
            r = self.client.post('products', data=dict(
                code='code' + i,
                name='name' + i,
                price='1.0' + i,
            ))
            assert r.status_code == 201, "Product POST failed"

        r = self.client.get('products')
        assert r.status_code == 200
        assert len(r.json) == 3, "Expected 3 products but got {0}".format(
            len(r.json))
        for f in ['id', 'code', 'name', 'price', 'active']:
            assert f in r.json[0]
