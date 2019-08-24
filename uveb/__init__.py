from flask import Flask
from flask_restful import Api
from flask_mail import Mail
from flask_cors import CORS
from mysql.connector import connect

app = Flask(__name__)
app.config.from_pyfile('config.py')
CORS(app)
mail = Mail(app)
api = Api(app)

from uveb.controllers.db import Init
from uveb.resources.index import IndexResource


api.add_resource(IndexResource, '/')


@app.before_first_request
def before_first_request():
    conn = connect(
        host=app.config['DB_HOST'],
        user=app.config['DB_USER'],
        password=app.config['DB_PASS'],
        database=app.config['DB_SCHEMA']
    )
    Init.init(conn)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST')
    return response

