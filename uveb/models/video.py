# Video Model


class VideoModel:
    """Represent a video"""

    def __init__(self, user_id, title, author, description, duration, track_id, resolution,
                 dir, size, date, id=None, likes=0, views=0, hotness=0):
        self.user_id = user_id
        self.title = title
        self.author = author
        self.description = description
        self.duration = duration
        self.track_id = track_id
        self.resolution = resolution
        self.dir = dir
        self.size = size
        self.date = date

        self.id = id
        self.likes = likes
        self.views = views
        self.hotness = hotness

    def serialize(self, tag=None):
        if tag:
            return {
                'id': self.id,
                'userId': self.user_id,
                'title': self.title,
                'description': self.description,
                'duration': self.duration,
                'trackId': self.track_id,
                'resW': self.resolution[0],
                'resH': self.resolution[1],
                'dir': self.dir,
                'size': self.size,
                'likes': self.likes,
                'views': self.views,
                'hotness': self.hotness,
                'tags': tag.serialize()
            }
        return {
            'id': self.id,
            'userId': self.user_id,
            'title': self.title,
            'description': self.description,
            'duration': self.duration,
            'trackId': self.track_id,
            'resW': self.resolution[0],
            'resH': self.resolution[1],
            'dir': self.dir,
            'size': self.size,
            'likes': self.likes,
            'views': self.views,
            'hotness': self.hotness,
        }

