# Video Tag Model


class TagModel:
    """Represent the tags of a video"""

    def __init__(self, video_id, track_id, id=None):
        self.video_id = video_id
        self.track_id = track_id

        self.id = id

    def serialize(self):
        return {
            'id': self.id,
            'videoId': self.video_id,
            'trackId': self.track_id
        }


