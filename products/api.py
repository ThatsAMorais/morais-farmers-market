import os

from flask import Flask, request, jsonify
from products.service import Service as product_service


app = Flask(__name__)
# TODO: sqlalchemy


@app.route('/products', methods=['POST'])
def create_product():
    return jsonify(product_service.get_product())


@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    return jsonify(product_service.get_product(id))


@app.route('/product/<id>', methods=['PUT'])
def put_product(id):
    return ('', 204)


@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    pass


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.getenv("MARKET_PRODUCTS_PORT", "15010"))
