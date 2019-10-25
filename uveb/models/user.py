import os
from passlib.apps import custom_app_context as pwd_context

from .. import app
from . import Models


class UserModel(Models):
    def __init__(self, username, email, password_hash, id=None,
                 identity=None, date=None, num_video=None, authenticated=None,
                 thumb_image=None, medium_image=None):
        self.username = username
        self.email = email
        self.password_hash = password_hash

        self.id = id
        self.identity = identity
        self.date = date
        self.num_video = num_video
        self.authenticated = authenticated
        self.thumb_image = thumb_image
        self.medium_image = medium_image

    @classmethod
    def init(cls, username, email, password):
        u = cls(username, email, password, date=cls.now(), authenticated=1)
        u.hash_password(u.password_hash).identify()

        return u

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        self._username = username

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email

    @property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password_hash):
        self._password_hash = password_hash

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def identity(self):
        return self._identity

    @identity.setter
    def identity(self, identity):
        self._identity = identity

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        self._date = date.strftime("%Y-%m-%d")

    @property
    def num_video(self):
        return self._num_video

    @num_video.setter
    def num_video(self, num_video):
        self._num_video = num_video

    @property
    def authenticated(self):
        return self._authenticated

    @authenticated.setter
    def authenticated(self, authenticated):
        self._authenticated = authenticated

    @property
    def thumb_image(self):
        return self._thumb_image

    @thumb_image.setter
    def thumb_image(self, thumb_image):
        self._thumb_image = thumb_image

    @property
    def medium_image(self):
        return self._medium_image

    @medium_image.setter
    def medium_image(self, medium_image):
        self._medium_image = medium_image

    def set_path(self, filename):
        self.thumb_image = f"https://{app.config['MAIN_BUCKET']}.{app.config['ENDPOINT']}/{self.id}" \
            f"/profile/{filename}"

    def identify(self):
        self.identity = Models.map(self.email)
        return self

    def hash_password(self, password):
        self.password_hash = pwd_context.hash(password)
        return self

    def verify_password_hash(self, password):
        return pwd_context.verify(password, self.password_hash)

    def serialize(self, full=False):
        if full:
            return {
                'id': self.id,
                'username': self.username,
                'email': self.email,
                'identity': self.identity,
                'password_hash': self.password_hash,
                'date': self.date,
                'numVideos': self.num_video,
                'authenticated': self.authenticated,
                'thumbImage': self.thumb_image,
                'mediumImage': self.medium_image
            }

        else:
            return {
                'id': self.id,
                'username': self.username,
                'email': self.email,
                'identity': self.identity,
                'date': self.date,
                'numVideos': self.num_video,
                'authenticated': self.authenticated,
                'thumbImage': self.thumb_image,
                'mediumImage': self.medium_image
            }




