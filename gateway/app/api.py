import os

import requests
from flask import Flask, jsonify, request


products_service_host = os.getenv('PRODUCT_SERVICE_HOST')
carts_service_host = os.getenv('CART_SERVICE_HOST')


api = Flask(__name__)


@api.route('/carts', methods=['POST'])
def create_cart():
    r = requests.post(carts_service_host + '/carts')
    return (r.json, 201)


@api.route('/cart/<id>', methods=['GET'])
def get_cart(id):
    url = carts_service_host + '/cart/' + id
    cart = requests.get(url).json
    total = requests.patch(url + '/invoice').json['total']
    return (jsonify(dict(total=total, cart=cart)), 200)


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
    url = carts_service_host + '/cart/' + id
    data = dict(add=request.form.get('add'), remove=request.form.get('remove'))
    cart = requests.patch(url, data=data).json
    total = requests.patch(url + '/invoice').json['total']
    return (jsonify(dict(total=total, cart=cart)), 200)


@api.route('/cart/<id>/invoice', methods=['GET'])
def get_cart_invoice(id):
    return (requests.patch(carts_service_host + '/cart/' + id + '/invoice').json, 200)


@api.route('/products', methods=['GET'])
def get_products():
    r = requests.get(products_service_host + '/products')
    return (r.json, 200)
