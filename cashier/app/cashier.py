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
                return ('Bad Request: No cart given')

            # Build a basic price invoice without specials from the cart and product-price data
            products = [requests.get(
                '{0}/product/{1}'.format(self.products_service, x)).json() for x in set(cart)]
            product_prices = dict((p['code'], float(p['price']))
                                  for p in products)

            # Apply the specials to the items
            items, total = specials.apply_specials(
                self.db.specials.find(), cart, product_prices)

            return (jsonify(dict(invoice=dict(items=items,
                                              total=total))),
                    200)

    def start(self):
        self.api.run(debug=True, host='0.0.0.0', port=self.port)
