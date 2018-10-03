
import requests
from flask import Flask  # , request, jsonify


api = Flask(__name__)


@api.route('/carts', methods=['POST'])
def create_cart():
    # return jsonify(cart_service.get_cart())
    pass


@api.route('/cart/<id>', methods=['GET'])
def get_cart(id):
    # return jsonify(cart_service.get_cart(id))
    pass


@api.route('/cart/<id>', methods=['PATCH'])
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
    # TODO
    # cart_service.add_items(id, request.form.get('add'))
    # cart_service.remove_items(id, request.form.get('remove'))
    # total = cart_service.invoice['total']
    return ('', 204)


@api.route('/cart/<id>/invoice', methods=['GET'])
def get_cart_invoice(id):
    # total = cart_service.invoice['total']
    pass


@api.route('/products', methods=['GET'])
def get_products():
    r = requests.get('https://products')
    return r.json
