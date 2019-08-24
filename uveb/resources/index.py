from flask import jsonify
from flask_restful import Resource

from . import app


class IndexResource(Resource):
    @staticmethod
    def get():
        return jsonify({
            'Project_Name': app.config['PROJECT_NAME'],
            'Version': app.config['VERSION']
        })

