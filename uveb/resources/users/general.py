from flask import request, session, jsonify, make_response
from flask_restful import Resource

from .. import UserModel
from .. import UserFetcher, UserAdder, UserUpdater
from .. import Validate, SendMail
from .. import gen_code


class UserInfoResource(Resource):
    @staticmethod
    def get():
        if 'id' in session:
            user = UserFetcher.fetch_by_id(session['id'])
            session['username'] = user.username
            session['email'] = user.email

            return jsonify({'user': user.serialize()})

        else:
            session.clear()
            return jsonify({'user': None})


class VerifyPasswordResource(Resource):
    @staticmethod
    def post():
        if 'email' not in session:
            return jsonify({'status': 3005})

        param = Validate.request(('password',), request.get_json())
        if type(param) == int:
            return jsonify({'status': param})

        user = UserFetcher.fetch({'email': session['email']})
        if not user.verify_password_hash(param['password']):
            return jsonify({'status': 3000})

        else:
            session['id'] = user.id

            return jsonify({'status': 2000})


class CreatePasswordResource(Resource):
    @staticmethod
    def post():
        if 'email' not in session and 'username' not in session:
            return jsonify({'status': 3005})

        param = Validate.request(('password',), request.get_json())
        if type(param) == int:
            return jsonify({'status': param})

        user = UserFetcher.fetch({'email': session['email']})
        if not user:
            UserAdder.insert(UserModel.init(session['username'],
                                            session['email'],
                                            param['password']).serialize(full=True))
            user = UserFetcher.fetch({'email': session['email']})

        else:
            UserUpdater.update(user.hash_password(param['password']).serialize(full=True),
                               {'email': session['email']})
            SendMail.notice_password_change(session)

        session['id'] = user.id

        return jsonify({'status': 2000})


class ResendCodeResource(Resource):
    @staticmethod
    def get():
        if 'code' in session and 'email' in session and 'username' in session:
            session['code'] = gen_code()
            SendMail.auth(session, session['code'])

            return jsonify({'status': 2000})
        return jsonify({'status': 3005})


class AuthCodeResource(Resource):
    @staticmethod
    def post():
        if 'code' not in session:
            return jsonify({'status': 3005})

        param = Validate.request(('code',), request.get_json())
        if type(param) == int:
            return jsonify({'status': param})

        if session['code'] != int(param['code']):
            return jsonify({'status': 3006})

        else:
            if 'id' in session:
                user = UserFetcher.fetch_by_id(session['id'])
                user.authenticated = 1
                user.identify()
                UserUpdater.update(user.serialize(), {'id': session['id']})

            session.pop('code')
            return jsonify({'status': 2000})


class SignUpResource(Resource):
    @staticmethod
    def post():
        param = Validate.request(('username', 'email'), request.get_json())
        if type(param) == int:
            return jsonify({'status': param})

        res = Validate.user_duplicate(param)
        if res != 2000:
            return jsonify({'status': res})

        session['code'] = gen_code()
        session['email'] = param['email']
        session['username'] = param['username']
        SendMail.auth(param, session['code'])

        return jsonify({'status': 2000})


class LoginResource(Resource):
    @staticmethod
    def post():
        params = request.get_json()
        if ('username' not in params and 'email' not in params) or len(params) != 1:
            return jsonify({'status': 3008})

        user = UserFetcher.fetch(params)
        if not user:
            return jsonify({'status': 3001})

        else:
            session['username'] = user.username
            session['email'] = user.email

            return jsonify({'status': 2000})


class ForgetPasswordResource(Resource):
    @staticmethod
    def post():
        param = Validate.request(('email',), request.get_json())
        if type(param) == int:
            return jsonify({'status': param})

        user = UserFetcher.fetch(param)
        if not user:
            return jsonify({'status': 3001})

        session['code'] = gen_code()
        session['email'] = user.email
        session['username'] = user.username
        SendMail.forget_password(param, session['code'])

        return jsonify({'status': 2000})
