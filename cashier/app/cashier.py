import requests
from flask import Flask, jsonify, request
from pymongo import MongoClient

from app import specials


class API:

    def __init__(self, port, mongo_host, products_host):
        self.port = port
        self.api = cashier = Flask(__name__)
        self.mongodb = MongoClient(f'mongodb://{mongo_host}:27017/market')
        self.products_service = products_host
        self.db = self.mongodb.market

        @cashier.route('/cashier/specials', methods=['GET'])
        def get_specials():
            """Retrieve the available specials"""
            return (jsonify(dict(specials=list(self.db.specials.find()))),
                    200)

        @cashier.route('/cashier/invoice', methods=['GET'])
        def get_invoice():
            """Given a cart of items, determine the price modifiers"""
            cart = request.args.getlist('cart')
            if not cart:
                return ('Bad Request: No cart given', 400)

            # Retrieve the product data
            all_products = requests.get('{0}/products'.format(self.products_service)).json()
            product_prices = dict((p['code'], float(p['price'])) for p in all_products)

            # Apply the specials to the items
            items, total = specials.apply_specials(
                self.db.specials.find(), cart, product_prices)

            return (jsonify(dict(invoice=dict(items=items,
                                              total=total))),
                    200)

        @cashier.route('/health-check', methods=['GET'])
        def health_check():
            """Verifies the health of dependent services"""
            # Note: MongoClient handles connectivity with mongo well
            try:
                # Verify health of Products service
                r = requests.get(self.products_service + '/health-check')
                if r.status_code != 200:
                    return ('Service Unavailable', 503)
                    print('Connection to Products Service: FAIL')
            except requests.exceptions.ConnectionError:
                return ('Service Unavailable', 503)
                print('Connection to Products Service: FAIL')
            print('Connection to Products Service: OK')
            return ('', 200)

    def start(self):
        self.api.run(debug=True, host='0.0.0.0', port=self.port)
