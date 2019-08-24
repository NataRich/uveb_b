from flask import jsonify
from flask_restful import Resource


class IndexResource(Resource):
    @staticmethod
    def get():
        return jsonify({
            'Project Name': 'uveb',
            'Version': '0.0.3'
        })

