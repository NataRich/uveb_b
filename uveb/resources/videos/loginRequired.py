from flask import request, session, jsonify
from flask_restful import Resource
import ffmpeg

from .. import app
from .. import VideoModel, TagModel
from .. import UserUpdater
from .. import VideoFetcher, VideoAdder, VideoDeleter
from .. import TagFetcher, TagAdder
from .. import login_required, AWS, Validate
from .. import gen_key


class UploadOneVideoResource(Resource):
    @staticmethod
    @login_required
    def post():
        if 'file' not in request.files:
            return jsonify({'status': 3008})

        video = request.files['file']

        AWS.get_video_info(video.read())

        ext = video.filename.split('.')[1]
        if not AWS.is_ext_allowed(ext, 'video'):
            return jsonify({'status': 3007})

        track_id = gen_key()
        if not AWS.upload_video(video, session['id'], gen_key()):
            return jsonify({'status': 4444})

        session['TRACK_ID'] = track_id
        session['KEY'] = 'users/' + str(session['id']) + '/videos/' + track_id + '/original.' + ext
        session['VIDEO_SIZE'] = video.content_length
        return jsonify({'status': 2000})

    @staticmethod
    @login_required
    def get():
        if 'TRACK_ID' in session:
            return jsonify({'status': 3009})

        if not AWS.remove_video(session['TRACK_ID'], session['id']):
            return jsonify({'status': 4444})

        session.pop('TRACK_ID')
        return jsonify({'status': 2000})


class UploadVideoInfoResource(Resource):
    @staticmethod
    @login_required
    def post():
        params = Validate.request(('title', 'description', 'tags'), request.get_json())
        if type(params) == int:
            return jsonify({'status': params})

        v = VideoModel.init(session['id'], params['title'], session['username'], params['description'],
                            session['TRACK_ID'])
        c_info = AWS.get_video_info(session['KEY']).copy()
        c_info.update({'size': session['VIDEO_SIZE']})
        v.update_i(c_info)
        VideoAdder.insert(v.serialize())

        v = VideoFetcher.fetch_by_track_id(session['TRACK_ID'])
        t = TagModel(v.id, v.track_id, params['tags']['vr'], params['tags']['campus'], params['tags']['event'])
        TagAdder.insert(t.serialize())

        UserUpdater.update_num_videos(session['id'])
        session.pop('TRACK_ID')
        session.pop('KEY')
        session.pop('VIDEO_SIZE')
        return jsonify({'status': 2000})


class SelfUploadedVideoResource(Resource):
    @staticmethod
    @login_required
    def post():
        params = Validate.request(('page', 'sort_by', 'order'), request.get_json())
        if type(params) == int:
            return jsonify({'status': params})

        vs = VideoFetcher.fetch_all_by_user_id(session['id'], offset=(params['page'] - 1) * 5,
                                               by_col=params['sort_by'], asc=params['order'])
        if not vs:
            return jsonify({'status': 3011, 'videos': []})

        cvs = [cv.serialize(tags=TagFetcher.fetch_by_video_id(cv.id)) for cv in vs]
        return jsonify({'status': 2000, 'videos': cvs})


class DeleteVideoResource(Resource):
    @staticmethod
    @login_required
    def post():
        param = Validate.request(('video_id',), request.get_json())
        if type(param) == int:
            return jsonify({'status': param})

        v = VideoFetcher.fetch_by_video_id(param['video_id'])
        if not v:
            return jsonify({'status': 3011})

        AWS.remove_video(v.track_id, session['id'])
        VideoDeleter.delete(v.track_id)
        return jsonify({'status': 2000})

