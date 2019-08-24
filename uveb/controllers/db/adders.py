from contextlib import closing

from . import Adders, AutoSQL


class UserAdder(Adders):
    @classmethod
    def insert(cls, user_dict):
        cols = AutoSQL.get_columns(cls.USER_T, skip=('id', 'numVideos', 'thumbImage', 'mediumImage'))
        vals = AutoSQL.gen_syntax(cls.USER_T, user_dict, tuplize=True)

        with closing(cls.conn.cursor()) as cur:
            cur.execute(f"""INSERT INTO {cls.USER_T} {cols} VALUES {vals}""")
            cls.conn.commit()


class VideoAdder(Adders):
    @classmethod
    def insert(cls, video_dict):
        cols = AutoSQL.get_columns(cls.VIDEOS_T, skip=('id', 'likes', 'views', 'hotness'))
        vals = AutoSQL.gen_syntax(cls.VIDEOS_T, video_dict, tuplize=True)

        with closing(cls.conn.cursor()) as cur:
            cur.execute(f"""INSERT INTO {cls.VIDEOS_T} {cols} VALUES {vals}""")
            cls.conn.commit()


class TagAdder(Adders):
    @classmethod
    def insert(cls, tag_dict):
        cols = AutoSQL.get_columns(cls.TAGS_T, skip=('id',))
        vals = AutoSQL.gen_syntax(cls.TAGS_T, tag_dict, tuplize=True)

        with closing(cls.conn.cursor()) as cur:
            cur.execute(f"""INSERT INTO {cls.TAGS_T} {cols} VALUES {vals}""")
            cls.conn.commit()
