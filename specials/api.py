import os

from flask import Flask, request, jsonify
from specials.service import Service as specials_service


app = Flask(__name__)


@app.route('/specials', methods=['POST'])
def create_special():
    return jsonify(special_service.get_special())


@app.route('/special/<id>', methods=['GET'])
def get_special(id):
    return jsonify(special_service.get_special(id))


@app.route('/special/<id>', methods=['PUT'])
def put_special(id):
    # TODO
    return ('', 204)


@app.route('/special/<id>', methods=['DELETE'])
def delete_special(id):
    pass


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.getenv("MARKET_SPECIALS_PORT", "15100"))
