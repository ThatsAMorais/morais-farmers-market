"""
Verify behavior of the API
"""
import os
import time

from flask_testing import TestCase

from app.cashier import API

# TODO: Better isolation from the other services, but using docker-compose is fine for now


class MyTest(TestCase):

    def create_app(self):
        self.api = API(port=os.getenv("MARKET_CASHIER_PORT", "15100"),
                       mongo_host=os.getenv('DOC_STORE_HOST', 'doc-store'),
                       products_host=os.getenv('PRODUCT_SERVICE_HOST'))
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
            time.sleep(5)

    def tearDown(self):
        pass

    def test_get_invoice(self):
        """Verify cart invoice interface"""
        cart = ['AP1', 'AP1', 'AP1',  'CH1', 'MK1', 'OM1', 'OM1', 'CF1', 'CF1']
        query_params = '&'.join(['cart={0}'.format(x) for x in cart])
        r = self.client.get('/cashier/invoice?' + query_params)
        jsn = r.json
        assert r.status_code == 200
        assert 'invoice' in jsn, 'Expected response to contain "invoice"'
        assert 'total' in jsn['invoice'], 'Expected total in invoice response'
        assert 'items' in jsn['invoice'], 'Expected items in invoice response'
