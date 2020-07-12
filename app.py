import os
from flask import Flask, render_template
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask import jsonify, request
from bson import ObjectId

import json
from bson import json_util

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')

CORS(app)

app.config["MONGO_URI"] = "mongodb+srv://vlad123:qwerty123@tic-tac-toe-jtwsd.mongodb.net/pizza-stock?retryWrites=true&w=majority"
app.config['SECRET_KEY'] = 'hero'

mongo = PyMongo(app)

@app.route('/')
def home():
    return 'Deployed'


@app.route("/products", methods=['GET'])
def getProducts():
    stock = mongo.db["pizza-stock"]
    items = list(stock.find())
    for item in items:
        item.update({"id": str(item['_id'])})
        del item["_id"]
    return jsonify(items)


@app.route("/product", methods=['GET'])
def getProduct():
    stock = mongo.db["pizza-stock"]
    id = request.args.get("id")
    output = []
    for s in stock.find({"_id": ObjectId(id)}):
        output.append({'price': s['price'], 'title': s['title'], "id": str(s['_id']), 'description': s['description'],
                       'img': s['img'], 'type': s['type'], 'ingredients': s['ingredients']})
    return jsonify(output)


@app.route("/ingredients", methods=['GET'])
def getIngredients():
    stock = mongo.db["ingredients"]
    output = []
    for s in stock.find({}):
        output.append({'price': s['price'], 'name': s['name'], "id": str(s['_id'])})
    return jsonify(output)

@app.route("/order", methods=["GET"])
def getOrders():
    phoneNumber = request.args.get("phoneNumber")
    orders = mongo.db["orders"]
    items = list(orders.find({"orderInfo.phoneNumber": int(phoneNumber)}))
    for item in items:
        item.update({"id": str(item['_id'])})
        del item["_id"]
    return jsonify(items)

@app.route("/order", methods=["POST"])
def createOrder():
    parsed_string = json.loads(request.data)
    mongo.db.orders.insert(parsed_string)
    return 'OK'

@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
