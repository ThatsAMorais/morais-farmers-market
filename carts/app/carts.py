
import json

from flask import Flask, jsonify, request


class API:

    def __init__(self, port, store):

        self.port = port
        self.store = store
        self.api = carts = Flask(__name__)

        @carts.route('/carts', methods=['POST'])
        def create_cart():
            """
            Create a new cart
            Body:
            {
                'items': {
                    <product_code>: quantity>, ...
                }
            }
            """
            data = json.loads(request.data) if request.data else dict()
            return (jsonify(self.store.update_cart(None, data.get('items', dict()))),
                    201)

        @carts.route('/cart/<id>', methods=['GET'])
        def get_cart(id):
            """Retrieve a cached cart"""
            return (jsonify(self.store.get_cart(id)),
                    200)

        @carts.route('/cart/<id>', methods=['POST'])
        def patch_cart(id):
            """
            Add items to the cart
            Body:
            {
                'add': {
                    <product_code>: <quantity>, ...
                },
                'remove': {
                    <product_code>: <quantity>, ...
                }
            }
            """
            data = json.loads(request.data) if request.data else dict()
            return (jsonify(self.store.update_cart(id, data.get('add', dict()), data.get('remove', dict()))),
                    200)

        @carts.route('/cart/<id>', methods=['DELETE'])
        def delete_cart(id):
            """Remove a cart manually"""
            self.store.delete_cart()
            ('', 204)

        @carts.route('/health-check', methods=['GET'])
        def health_check():
            """Check health of dependencies"""
            if not self.store.health_check():
                return ('Service Unavailable', 503)
            return ('', 200)

    def start(self):
        self.api.run(debug=True, host='0.0.0.0', port=self.port)
