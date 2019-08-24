from contextlib import closing

from . import Deleters


class UserDeleter(Deleters):
    @classmethod
    def delete(cls, username):
        with closing(cls.conn.cursor()) as cur:
            cur.execute(f"""DELETE FROM {cls.USER_T} WHERE username='{username}'""")
            cls.conn.commit()


class VideoDeleter(Deleters):
    @classmethod
    def delete(cls, track_id):
        with closing(cls.conn.cursor()) as cur:
            cur.execute(f"""DELETE FROM {cls.VIDEOS_T} WHERE trackId='{track_id}'""")
            cls.conn.commit()



