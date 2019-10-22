# /uveb/resources/__init__.py
from functools import wraps
from flask import session, jsonify

from .. import app, mail
from ..models.user import UserModel
from ..models.video import VideoModel
from ..models.tag import TagModel
from ..controllers.auth.mails import SendMail
from ..controllers.auth.validate import Validate
from ..controllers.db.fetchers import UserFetcher, VideoFetcher, TagFetcher
from ..controllers.db.adders import UserAdder, VideoAdder, TagAdder
from ..controllers.db.updaters import UserUpdater, VideoUpdater
from ..controllers.db.deleters import UserDeleter, VideoDeleter
from ..controllers.ali.ali import AliCloudService
from ..utility.utils import gen_code


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'id' not in session:
            return jsonify({'status': 3005})

        elif not UserFetcher.fetch({'id': session['id']}):
            session.clear()
            return jsonify({'status': 3005})

        else:
            try:
                return f(*args, **kwargs)

            except Exception as e:
                print('request err', e)
                return jsonify({'status': 4444})
    return wrap



