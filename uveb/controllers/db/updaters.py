from contextlib import closing

from . import Updaters, AutoSQL


class UserUpdater(Updaters):
    @classmethod
    def update(cls, set_key, key):
        new = AutoSQL.gen_syntax(cls.USER_T, set_key)
        loc = AutoSQL.gen_syntax(cls.USER_T, key, AND=True)

        with closing(cls.conn.cursor()) as cur:
            cur.execute(f"""UPDATE {cls.USER_T} SET {new} WHERE {loc}""")
            cls.conn.commit()

    @classmethod
    def update_num_videos(cls, user_id):
        with closing(cls.conn.cursor()) as cur:
            cur.execute(f"""SELECT count(*) FROM {cls.VIDEOS_T} WHERE userId={user_id}""")
            n = cur.fetchone()[0]

            cur.execute(f"""UPDATE {cls.USER_T} SET numVideos={n} WHERE id={user_id}""")
            cls.conn.commit()


class VideoUpdater(Updaters):
    @classmethod
    def update(cls, set_key, key):
        new = AutoSQL.gen_syntax(cls.VIDEOS_T, set_key)
        loc = AutoSQL.gen_syntax(cls.VIDEOS_T, key, AND=True)

        with closing(cls.conn.cursor()) as cur:
            cur.execute(f"""UPDATE {cls.VIDEOS_T} SET {new} WHERE {loc}""")
            cls.conn.commit()



