from . import Models


class TagModel(Models):
    def __init__(self, video_id, track_id, vr, campus, event, id=None):
        self.video_id = video_id
        self.vr = vr
        self.campus = campus
        self.event = event
        self.track_id = track_id

        self.id = id

    @property
    def video_id(self):
        return self._video_id

    @video_id.setter
    def video_id(self, video_id):
        self._video_id = video_id

    @property
    def track_id(self):
        return self._track_id

    @track_id.setter
    def track_id(self, track_id):
        self._track_id = track_id

    @property
    def vr(self):
        return self._vr

    @vr.setter
    def vr(self, vr):
        self._vr = vr

    @property
    def campus(self):
        return self._campus

    @campus.setter
    def campus(self, campus):
        self._campus = campus

    @property
    def event(self):
        return self._event

    @event.setter
    def event(self, event):
        self._event = event

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    def serialize(self, append=False):
        if append:
            return {
                "tags": {
                    "vr": self.vr,
                    'campus': self.campus,
                    'event': self.event
                }
            }
        return {
            'id': self.id,
            'videoId': self.video_id,
            'trackId': self.track_id,
            'vr': self.vr,
            'campus': self.campus,
            'event': self.event
        }
