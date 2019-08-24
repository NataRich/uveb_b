# User Model
from passlib.apps import custom_app_context as pwd_context
from datetime import datetime


class UserModel:
    """Represent a user"""

    MAP_IDENTITY = {
        'uwcchina.org': 8888,
    }

    def __init__(self, username, email, identity, password_hash, date, id=None, num_videos=0,
                 authenticated=0, thumb_image=None, medium_image=None):
        self.username = username
        self.email = email
        self.identity = identity
        self.password_hash = password_hash
        self.date = date

        self.id = id
        self.num_videos = num_videos
        self.authenticated = authenticated
        self.thumb_image = thumb_image
        self.medium_image = medium_image

    @classmethod
    def init(cls, username, email, password):
        identity = 1111
        password_hash = cls.hash_password(password)
        date = datetime.today().strftime("%Y-%m-%d")
        return cls(username, email, identity, password_hash, date)

    @classmethod
    def identify(cls, email):
        domain = email.split('@')[1]
        return cls.MAP_IDENTITY[domain] if domain in cls.MAP_IDENTITY else 1111

    @staticmethod
    def hash_password(password):
        return pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'identity': self.identity,
            'password_hash': self.password_hash,
            'date': self.date,
            'numVideos': self.num_videos,
            'authenticated': self.authenticated,
            'thumbImage': self.thumb_image,
            'mediumImage': self.medium_image
        }


