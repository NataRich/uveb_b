from . import Models
from .. import app


class VideoProcessingException(Exception):
    pass


class VideoModel(Models):
    def __init__(self, user_id, title, author, description, track_id, dir=None,
                 duration=None, res_w=None, res_h=None, id=None, size=None,
                 date=None, likes=None, views=None, hotness=None):
        self.user_id = user_id
        self.title = title
        self.author = author
        self.description = description
        self.track_id = track_id
        self.dir = dir

        self.id = id
        self.duration = duration
        self.res_w = res_w
        self.res_h = res_h
        self.size = size
        self.date = date
        self.likes = likes
        self.views = views
        self.hotness = hotness

    @classmethod
    def init(cls, user_id, title, author, description, track_id):
        v = cls(user_id, title, author, description, track_id, date=cls.now())
        v.set_dir()
        return v

    def update_i(self, info):
        self.duration = info['duration']
        self.res_w = info['width']
        self.res_h = info['height']
        self.size = info['size']
        return self

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        self._user_id = user_id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, author):
        self._author = author

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def track_id(self):
        return self._track_id

    @track_id.setter
    def track_id(self, track_id):
        self._track_id = track_id

    @property
    def dir(self):
        return self._dir

    @dir.setter
    def dir(self, dir):
        self._dir = dir

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, duration):
        self._duration = str(duration)

    @property
    def res_w(self):
        return self._res_w

    @res_w.setter
    def res_w(self, res_w):
        self._res_w = res_w

    @property
    def res_h(self):
        return self._res_h

    @res_h.setter
    def res_h(self, res_h):
        self._res_h = res_h

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        self._size = size

    @property
    def date(self):
        return self._date.strftime("%Y-%m-%d %H:%M:%S")

    @date.setter
    def date(self, date):
        self._date = date

    @property
    def likes(self):
        return self._likes

    @likes.setter
    def likes(self, likes):
        self._likes = likes

    @property
    def views(self):
        return self._views

    @views.setter
    def views(self, views):
        self._views = views

    @property
    def hotness(self):
        return self._hotness

    @hotness.setter
    def hotness(self, hotness):
        self._hotness = hotness

    def set_dir(self):
        self.dir = app.config['UPLOAD_PATH'] + f"{str(self.user_id)}/videos/{self.track_id}/"

    def serialize(self):
        return {
            'userId': self.user_id,
            'title': self.title,
            'author': self.author,
            'description': f"""{self.description}""",
            'id': self.id,
            'duration': self.duration,
            'trackId': self.track_id,
            'resW': self.res_w,
            'resH': self.res_h,
            'dir': self.dir,
            'size': self.size,
            'date': self.date,
            'likes': self.likes,
            'views': self.views,
            'hotness': self.hotness,
        }
