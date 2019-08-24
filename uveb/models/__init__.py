from datetime import datetime


class Models:

    USER_T = 'users'
    VIDEOS_T = 'videos'
    TAGS_T = 'tags'

    ID_MAP = {
        'uwcchina.org':         8888,
        'uwcuvr.org':           9999,

        'g':                    1111
    }

    @classmethod
    def map(cls, email):
        if email:
            domain = email.split('@')[1]
            return cls.ID_MAP[domain] if domain in cls.ID_MAP else cls.ID_MAP['g']

    @staticmethod
    def now():
        return datetime.now()
