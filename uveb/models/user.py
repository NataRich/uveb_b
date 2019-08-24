# User Model


class UserModel:
    """Represent a user"""

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


