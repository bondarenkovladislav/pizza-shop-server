import os
from flask import Flask, render_template
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask import jsonify

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

@app.route("/get-stock")
def getStock():
    stock = mongo.db["pizza-stock"]
    stock_list = list(stock.find())
    return json.dumps(stock_list, default=json_util.default)

@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
