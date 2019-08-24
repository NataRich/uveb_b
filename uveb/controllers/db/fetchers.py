from contextlib import closing

from . import Fetchers, AutoSQL
from ..models.user import UserModel
from ..models.video import VideoModel
from ..models.tag import TagModel


class UserFetcher(Fetchers):
    @classmethod
    def fetch(cls, user_dict):
        key = AutoSQL.gen_syntax(cls.USER_T, user_dict, AND=True)

        with closing(cls.conn.cursor()) as cur:
            cur.execute(f"""SELECT * FROM {cls.USER_T} WHERE {key}""")
            r = cur.fetchone()

        if r:
            return UserModel(r[1], r[2], r[4], id=r[0], identity=r[3],
                             date=r[5], num_video=r[6], authenticated=r[7],
                             thumb_image=r[8], medium_image=r[9])

    @classmethod
    def fetch_by_id(cls, id):
        with closing(cls.conn.cursor()) as cur:
            cur.execute(f"""SELECT * FROM {cls.USER_T} WHERE id={id}""")
            r = cur.fetchone()

        if r:
            return UserModel(r[1], r[2], r[4], id=r[0], identity=r[3],
                             date=r[5], num_video=r[6], authenticated=r[7],
                             thumb_image=r[8], medium_image=r[9])


class VideoFetcher(Fetchers):
    @classmethod
    def fetch_all(cls, ids=(), limit=8, offset=0, by_col='date', asc=True, title=None):
        suffix = AutoSQL.add_suffix(limit=limit, offset=offset, asc=asc, by_col=by_col)
        key = AutoSQL.gen_special(ids, title)

        with closing(cls.conn.cursor()) as cur:
            cur.execute(f"""SELECT * FROM {cls.VIDEOS_T} WHERE {key} {suffix}""")
            rows = cur.fetchall()

        if rows:
            return [VideoModel(r[1], r[2], r[3], r[4], r[6], dir=r[9],
                               duration=r[5], res_w=r[7], res_h=r[8],
                               id=r[0], size=r[10], date=r[11], likes=r[12],
                               views=r[13], hotness=r[14]) for r in rows]

    @classmethod
    def fetch_all_by_user_id(cls, user_id, limit=5, offset=0, by_col='date', asc=True):
        suffix = AutoSQL.add_suffix(limit=limit, offset=offset, by_col=by_col, asc=asc)

        with closing(cls.conn.cursor()) as cur:
            cur.execute(f"""SELECT * FROM {cls.VIDEOS_T} WHERE userId={user_id}{suffix}""")
            rows = cur.fetchall()

        if rows:
            return [VideoModel(r[1], r[2], r[3], r[4], r[6], dir=r[9],
                               duration=r[5], res_w=r[7], res_h=r[8],
                               id=r[0], size=r[10], date=r[11], likes=r[12],
                               views=r[13], hotness=r[14]) for r in rows]

    @classmethod
    def fetch_by_track_id(cls, track_id):
        with closing(cls.conn.cursor()) as cur:
            cur.execute(f"""SELECT * FROM {cls.VIDEOS_T} WHERE trackId='{track_id}'""")
            r = cur.fetchone()

        if r:
            return VideoModel(r[1], r[2], r[3], r[4], r[6], dir=r[9],
                              duration=r[5], res_w=r[7], res_h=r[8],
                              id=r[0], size=r[10], date=r[11], likes=r[12],
                              views=r[13], hotness=r[14])

    @classmethod
    def fetch_by_video_id(cls, video_id):
        with closing(cls. conn.cursor()) as cur:
            cur.execute(f"""SELECT * FROM {cls.VIDEOS_T} WHERE id={video_id}""")
            r = cur.fetchone()

        if r:
            return VideoModel(r[1], r[2], r[3], r[4], r[6], dir=r[9],
                              duration=r[5], res_w=r[7], res_h=r[8],
                              id=r[0], size=r[10], date=r[11], likes=r[12],
                              views=r[13], hotness=r[14])


class TagFetcher(Fetchers):
    @classmethod
    def fetch(cls, any_dict):
        key = AutoSQL.gen_syntax(cls.TAGS_T, any_dict, AND=True)

        with closing(cls.conn.cursor()) as cur:
            cur.execute(f"""SELECT * FROM {cls.TAGS_T} WHERE {key}""")
            rows = cur.fetchall()

        if rows:
            return [TagModel(r[1], r[2], r[3], r[4], r[5], id=r[0]) for r in rows]

    @classmethod
    def fetch_by_video_id(cls, video_id):
        with closing(cls.conn.cursor()) as cur:
            cur.execute(f"""SELECT * FROM {cls.TAGS_T} WHERE videoId={video_id}""")
            r = cur.fetchone()

        if r:
            return TagModel(r[1], r[2], r[3], r[4], r[5], id=r[0])


