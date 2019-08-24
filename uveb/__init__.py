from flask import Flask
from flask_restful import Api
from flask_mail import Mail
from flask_cors import CORS
from mysql.connector import connect

app = Flask(__name__)
app.config.from_pyfile('config.py')

if app.config['ENV'] == 'development':
    app.config['DB_HOST'] = app.config['DEV_DB_HOST']
    app.config['DB_USER'] = app.config['DEV_DB_USER']
    app.config['DB_PASS'] = app.config['DEV_DB_PASS']
    app.config['DB_SCHEMA'] = app.config['DEV_DB_SCHEMA']

else:
    app.config['DB_HOST'] = app.config['PROD_DB_HOST']
    app.config['DB_USER'] = app.config['PROD_DB_USER']
    app.config['DB_PASS'] = app.config['PROD_DB_PASS']
    app.config['DB_SCHEMA'] = app.config['PROD_DB_SCHEMA']

CORS(app)
mail = Mail(app)
api = Api(app)

from uveb.controllers.db import Init
from uveb.resources.index import IndexResource


api.add_resource(IndexResource, '/')


@app.before_request
def before_request():
    conn = connect(
        host=app.config['DB_HOST'],
        user=app.config['DB_USER'],
        password=app.config['DB_PASS'],
        database=app.config['DB_SCHEMA']
    )
    Init.init(conn)


@app.after_request
def after_request(response):
    Init.conn.close()
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST')
    return response


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4000)
