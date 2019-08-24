from flask import Flask
from flask_restful import Api
from flask_mail import Mail
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
mail = Mail(app)
api = Api(app)

from uveb.resources.index import IndexResource


api.add_resource(IndexResource, '/')


@app.before_first_request
def before_first_request():
    init = None


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST')
    return response


if __name__ == '__main__':
    app.run(debug=True)

