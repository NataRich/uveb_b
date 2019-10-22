from flask import session, jsonify, request
from flask_restful import Resource

from .. import login_required
from .. import gen_code
from .. import Validate, SendMail, AliCloudService
from .. import UserFetcher, UserUpdater


class LogoutResource(Resource):
    @staticmethod
    @login_required
    def get():
        session.clear()
        return jsonify({'status': 2000})


class ChangeAccountResource(Resource):
    @staticmethod
    @login_required
    def get():
        username = request.args.get('username')
        res = Validate.user_duplicate({'username': username})
        if res != 2000:
            return jsonify({'status': res})

        user = UserFetcher.fetch_by_id(session['id'])
        user.username = username
        UserUpdater.update(user.serialize(), {'id': session['id']})
        return jsonify({'status': 2000})

    @staticmethod
    @login_required
    def post():
        param = Validate.request(('email',), request.get_json())
        if type(param) == int:
            return jsonify({'status': param})

        res = Validate.user_duplicate(param)
        if res != 2000:
            return jsonify({'status': res})

        user = UserFetcher.fetch_by_id(session['id'])
        user.email = param['email']
        user.authenticated = 0
        user.identity = 1111
        UserUpdater.update(user.serialize(), {'id': session['id']})

        session.clear()
        session['id'] = user.id
        session['email'] = user.email
        session['username'] = user.username
        session['code'] = gen_code()
        SendMail.auth(session, session['code'])
        return jsonify({'status': 2000})


class ChangeProfileImageResource(Resource):
    @staticmethod
    @login_required
    def post():
        if 'image' not in request.files:
            return jsonify({'status': 3008})

        image = request.files['image']
        ext = image.filename.split('.')[1]
        if not AliCloudService.is_ext_allowed(ext, 'image'):
            return jsonify({'status': 3007})

        key = f"users/{session['id']}/profile/{image.filename}"
        if not AliCloudService.upload_profile(image, key):
            return jsonify({'status': 4444})

        user = UserFetcher.fetch_by_id(session['id'])
        user.set_path(ext)
        UserUpdater.update(user.serialize(), {'id': session['id']})
        return jsonify({'status': 2000})

