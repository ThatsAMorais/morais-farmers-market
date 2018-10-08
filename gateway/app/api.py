import json

import requests
from flask import Flask, jsonify, request


class API:

    def __init__(self, port, products_service_host, carts_service_host, cashier_service_host):
        self.port = port
        self.products_service_host = products_service_host
        self.carts_service_host = carts_service_host
        self.cashier_service_host = cashier_service_host
        self.api = api = Flask(__name__)

        @api.route('/carts', methods=['POST'])
        def create_cart():
            """Generate a cart ID"""
            r = requests.post(self.carts_service_host + '/carts')
            return (jsonify(dict(total=0.0, cart=r.json())),
                    201)

        @api.route('/cart/<id>', methods=['GET'])
        def get_cart(id):
            """Retrieve a cart from the Cart Service and its total from the Cashier service"""
            url = carts_service_host + '/cart/' + id
            cart = requests.get(url).json()
            total = self._get_cart_total(cart['items'])
            return (jsonify(dict(total=total, cart=cart)),
                    200)

        @api.route('/cart/<id>', methods=['POST'])
        def update_cart(id):
            """
            Add/Remove items from the cart
            Body:
            {
                add: {
                    <product_code>: <quantity>,
                },
                remove: {
                    <product_code>: <quantity>,
                }
            }
            """
            request_data = json.loads(request.data) if request.data else dict()
            data = json.dumps(dict(add=request_data.get('add', {}),
                                   remove=request_data.get('remove', {})))
            # update the cart
            cart = requests.post(self.carts_service_host + '/cart/' + id,
                                 data=data).json()
            # determine the total
            total = self._get_cart_total(cart['items'])
            return (jsonify(dict(total=total, cart=cart)),
                    200)

        @api.route('/cart/<id>/invoice', methods=['GET'])
        def get_cart_invoice(id):
            """Retrieve a Cart's Invoice"""
            cart = requests.get(self.carts_service_host +
                                '/cart/' + id).json()['items']
            r = self._request_cart_invoice(cart)
            return (jsonify(r.json()), 200)

        @api.route('/products', methods=['GET'])
        def get_products():
            r = requests.get(self.products_service_host + '/products')
            if r.status_code != 200:
                return ('', r.status_code)
            return (jsonify(dict(products=r.json())), 200)

        @api.route('/health-check', methods=['GET'])
        def health_check():
            try:
                r = requests.get(self.products_service_host + '/health-check')
                if r.status_code != 200:
                    print('Connection to Product Service: FAIL')
                    return ('Service Unavailable', 503)
            except requests.exceptions.ConnectionError:
                print('Connection to Product Service: FAIL')
                return ('Service Unavailable', 503)
            print('Connection to Product Service: OK')

            try:
                r = requests.get(self.carts_service_host + '/health-check')
                if r.status_code != 200:
                    print('Connection to Carts Service: FAIL')
                    return ('Service Unavailable', 503)
            except requests.exceptions.ConnectionError:
                print('Connection to Carts Service: FAIL')
                return ('Service Unavailable', 503)
            print('Connection to Carts Service: OK')

            try:
                r = requests.get(self.cashier_service_host + '/health-check')
                if r.status_code != 200:
                    print('Connection to Cashier Service: FAIL')
                    return ('Service Unavailable', 503)
            except requests.exceptions.ConnectionError:
                return ('Service Unavailable', 503)
                print('Connection to Cashier Service: FAIL')
            return ('', 200)
            print('Connection to Cashier Service: OK')

    def _request_cart_invoice(self, cart):
        query_params = '&'.join(['cart={0}'.format(x) for x in cart])
        return requests.get(
            self.cashier_service_host + '/cashier' + '/invoice?' + query_params)

    def _get_cart_total(self, cart):
        r = self._request_cart_invoice(cart)
        if not cart:
            return 0.0
        if r.status_code != 200:
            total = 'Unavailable: Try again: {0}'.format(r.status_code)
        else:
            total = r.json()['invoice']['total']
        return total

    def start(self):
        self.api.run(debug=True, host='0.0.0.0', port=self.port)
