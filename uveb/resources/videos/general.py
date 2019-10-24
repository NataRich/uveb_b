from flask import request, jsonify
from flask_restful import Resource

from .. import VideoFetcher, TagFetcher, VideoUpdater
from .. import Validate


class MainPageVideosByPropResource(Resource):
    @staticmethod
    def post():
        params = Validate.request(('page', 'tags', 'sort_by', 'order', 'title'), request.get_json())
        if type(params) == int:
            return jsonify({'status': params, 'videos': []})

        if not params['tags']:
            vs = VideoFetcher.fetch_all(limit=8, offset=(params['page'] - 1)*8,
                                        by_col=params['sort_by'], asc=params['order'],
                                        title=params['title'])

        else:
            ts = TagFetcher.fetch(params['tags'])
            if not ts:
                vs = []

            else:
                vs = VideoFetcher.fetch_all(tuple([t.video_id for t in ts]), limit=8, offset=(params['page'] - 1)*8,
                                            by_col=params['sort_by'], asc=params['order'], title=params['title'])

        if not vs:
            return jsonify({'status': 3011, 'videos': []})

        c = [v.serialize(tags=TagFetcher.fetch_by_video_id(v.id)) for v in vs]
        return jsonify({'status': 2000, 'videos': c})


class WatchOneVideoResource(Resource):
    @staticmethod
    def get():
        track_id = request.args.get('track_id')
        v = VideoFetcher.fetch_by_track_id(track_id)
        if not v:
            return jsonify({'video': None})

        cv = v.serialize(tags=TagFetcher.fetch_by_video_id(v.id))
        return jsonify({'video': cv})


class UpdateVideoStatsResource(Resource):
    @staticmethod
    def post():
        params = Validate.request(('video_id', 'likes', 'views'), request.get_json())
        if type(params) == int:
            return jsonify({'status': params})

        v = VideoFetcher.fetch_by_video_id(int(params['video_id']))
        if not v:
            return jsonify({'status': 3011})

        v.likes = int(params['likes'])
        v.views = int(params['views'])
        VideoUpdater.update(v.serialize(), {'id': v.id})
        return jsonify({'status': 2000})
