import os

import requests
from flask import Flask, request, jsonify


app = Flask("Market-API")


@app.route('/carts', methods=['POST'])
def create_cart():
    return jsonify(cart_service.get_cart())


@app.route('/cart/<id>', methods=['GET'])
def get_cart(id):
    return jsonify(cart_service.get_cart(id))


@app.route('/cart/<id>', methods=['PATCH'])
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


@app.route('/cart/<id>/invoice', methods=['GET'])
def get_cart_invoice(id):
    # total = cart_service.invoice['total']
    pass


@app.route('/products', methods=['GET'])
def get_products():
    # product_service.get
    pass 


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.getenv("MARKET_GATEWAY_PORT", "15000"))
