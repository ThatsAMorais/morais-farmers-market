import os

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


products = Flask(__name__)
products.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
products.config['SQLALCHEMY_DATABASE_URI'] = '{dialect}://{user}:{password}@{host}/{db}'.format(**{
    'dialect': 'mysql+pymysql',
    'user': 'root',
    'password': os.getenv('MYSQL_ROOT_PASSWORD'),
    'host': os.getenv('PRODUCT_DB_HOST', 'db'),
    'db': 'market'})


db = SQLAlchemy(products)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(8), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<Product {0} - {1} (${2})>'.format(self.code, self.name, self.price)

    def to_dict(self):
        """Return a dictionary representation of this model."""
        return dict(id=str(self.id), code=self.code, name=self.name, price=self.price, active=self.active)


@products.route('/products', methods=['POST'])
def create_product():
    try:
        code = request.form['code']
        name = request.form['name']
        price = request.form['price']
    except KeyError:
        return ('Bad Request: POST requires code, name, and price', 400)
    product = Product(code=code, name=name, price=price)
    db.session.add(product)
    db.session.commit()
    return (jsonify(product.to_dict()), 201)


@products.route('/products', methods=['GET'])
def get_products():
    return jsonify([x.to_dict() for x in Product.query.all()])


@products.route('/product/<id>', methods=['GET'])
def get_product(id):
    return jsonify(Product.query.filter_by(id=id).first().to_dict())


@products.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    p = Product.query.filter_by(id=id)
    p.active = False
    return ('', 204)
