import string
import random

from ..controllers.db.fetchers import VideoFetcher


def gen_key(l=24):
    key = string.ascii_letters
    res = ''.join(random.choice(key) for i in range(l)) + str(id)

    if VideoFetcher.fetch_by_track_id(res):
        return gen_key()
    return res


def gen_code():
    return random.randint(10000, 99999)
