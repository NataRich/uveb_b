from flask import Flask
from flask_restful import Api
from flask_mail import Mail
from flask_cors import CORS
from mysql.connector import connect

app = Flask(__name__)
app.config.from_pyfile('config.py')

if app.config['ENV'] == 'development':
    app.config['DB_HOST'] = app.config['DEV_DB_HOST']
    app.config['DB_PORT'] = app.config['DEV_DB_PORT']
    app.config['DB_USER'] = app.config['DEV_DB_USER']
    app.config['DB_PASS'] = app.config['DEV_DB_PASS']
    app.config['DB_SCHEMA'] = app.config['DEV_DB_SCHEMA']

else:
    app.config['DB_HOST'] = app.config['PROD_DB_HOST']
    app.config['DB_PORT'] = app.config['PROD_DB_PORT']
    app.config['DB_USER'] = app.config['PROD_DB_USER']
    app.config['DB_PASS'] = app.config['PROD_DB_PASS']
    app.config['DB_SCHEMA'] = app.config['PROD_DB_SCHEMA']

CORS(app)
mail = Mail(app)
api = Api(app)

from uveb.controllers.db import Init
from uveb.resources.index import IndexResource
from uveb.resources.users.general import UserInfoResource, VerifyPasswordResource, CreatePasswordResource, \
    SignUpResource, LoginResource, ResendCodeResource, AuthCodeResource, ForgetPasswordResource
from uveb.resources.users.loginRequired import LogoutResource, ChangeAccountResource, ChangeProfileImageResource
from uveb.resources.videos.general import MainPageVideosByPropResource, WatchOneVideoResource, \
    UpdateVideoStatsResource
from uveb.resources.videos.loginRequired import CheckTrackIdResource, UploadOneVideoResource, \
    UploadVideoInfoResource, SelfUploadedVideoResource, DeleteVideoResource

api.add_resource(IndexResource, '/')

api.add_resource(UserInfoResource, '/user')
api.add_resource(SignUpResource, '/signup')
api.add_resource(LoginResource, '/login')
api.add_resource(VerifyPasswordResource, '/verify_password')
api.add_resource(CreatePasswordResource, '/create_password')
api.add_resource(ResendCodeResource, '/resend_code')
api.add_resource(AuthCodeResource, '/auth_code')
api.add_resource(ForgetPasswordResource, '/forget_password')

api.add_resource(LogoutResource, '/logout')
api.add_resource(ChangeAccountResource, '/profile/change_account')
api.add_resource(ChangeProfileImageResource, '/profile/change_image')

api.add_resource(MainPageVideosByPropResource, '/videos')
api.add_resource(WatchOneVideoResource, '/videos/fetch')
api.add_resource(UpdateVideoStatsResource, '/videos/update_stats')

api.add_resource(CheckTrackIdResource, '/videos/track_id')
api.add_resource(UploadOneVideoResource, '/videos/upload_file')
api.add_resource(UploadVideoInfoResource, '/videos/upload_info')
api.add_resource(SelfUploadedVideoResource, '/videos/self_all')
api.add_resource(DeleteVideoResource, '/videos/delete_file')


@app.before_request
def before_request():
    conn = connect(
        host=app.config['DB_HOST'],
        user=app.config['DB_USER'],
        port=app.config['DB_PORT'],
        password=app.config['DB_PASS'],
        database=app.config['DB_SCHEMA']
    )
    Init.init(conn)


@app.after_request
def after_request(response):
    Init.conn.close()
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST')
    response.headers.add('Set-Cookie', 'HttpOnly; Secure; SameSite=None')
    return response


