import os

import requests

from flask import Flask, request, jsonify
from carts.service import Service as cart_service


app = Flask(__name__)


@app.route('/carts', methods=['POST'])
def create_cart():
    return jsonify(cart_service.get_cart())


@app.route('/cart/<id>', methods=['GET'])
def get_cart(id):
    return jsonify(cart_service.get_cart(id))


@app.route('/cart/<id>/add', methods=['PATCH'])
def add_to_cart(id):
    """
    Add items to the cart
    Body:
    {
        <product_code>: <quantity>,
    }
    """
    cart_service.add_items(id, request.form)
    return ('', 204)

    
@app.route('/cart/<id>/remove', methods=['PATCH'])
def remove_from_cart(id):
    """
    Remove items from the cart
    Body:
    {
        <product_code>: <quantity>,
    }
    """
    cart_service.remove_items(id, request.form)
    return ('', 204)


@app.route('/cart/<id>/invoice', methods=['GET'])
def get_cart_invoice(id):
    # TODO: Get cart
    products = [x for x in cart_service.get_cart(cart_id)['items']]
    results = dict(total=0, items=dict(),)

    if invoice:
        return calculate_detailed_invoice(result)

    return result['total']


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.getenv("MARKET_CARTS_PORT", "15010"))
