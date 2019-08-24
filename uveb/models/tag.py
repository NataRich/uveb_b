# Video Tag Model


class TagModel:
    """Represent the tags of a video"""

    def __init__(self, video_id, track_id, id=None, campus=0, vr=0, event=0):
        self.video_id = video_id
        self.track_id = track_id

        self.id = id
        self.campus = campus
        self.vr = vr
        self.event = event

    def serialize(self):
        return {
            'id': self.id,
            'videoId': self.video_id,
            'trackId': self.track_id,
            'campus': self.campus,
            'vr': self.vr,
            'event': self.event
        }


