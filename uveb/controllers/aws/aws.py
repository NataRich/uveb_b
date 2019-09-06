import boto3
import ffmpeg
from datetime import timedelta

from uveb import app


s3 = boto3.client('s3',
                  aws_access_key_id=app.config['AWS_ACCESS_KEY'],
                  aws_secret_access_key=app.config['AWS_SECRET_KEY'])
Bucket = app.config['BUCKET']


class AWS:
    @staticmethod
    def is_ext_allowed(ext, file_type):
        if file_type == 'image':
            return True if ext in app.config['IMAGE_EXTENSIONS_ALLOWED'] else False

        elif file_type == 'video':
            return True if ext in app.config['VIDEO_EXTENSIONS_ALLOWED'] else False

        else:
            return False

    @staticmethod
    def upload_profile(img_obj, user_id):
        try:
            ext = img_obj.filename.split('.')[1]
            key = 'users/' + str(user_id) + '/profile/original.' + ext
            s3.upload_fileobj(
                img_obj,
                Bucket,
                key,
                ExtraArgs={
                    'ContentType': img_obj.content_type
                }
            )

        except Exception as e:
            print('AWS IMG UPLOADING Error:', e)
            return False
        return True

    @staticmethod
    def upload_video(video_obj, user_id, track_id):
        try:
            ext = video_obj.filename.split('.')[1]
            key = 'users/' + str(user_id) + '/videos/' + track_id + '/original.' + ext
            s3.upload_fileobj(
                video_obj,
                Bucket,
                key,
                ExtraArgs={
                    'ContentType': video_obj.content_type
                }
            )

        except Exception as e:
            print('AWS VIDEO UPLOADING Error:', e)
            return False
        return True

    @staticmethod
    def get_video_info(video_obj):
        # print(s3.head_object(Bucket=Bucket, Key='users/2/videos/dHSaMhuVQgTtzhrwIyPhmDRy/original.mp4'))
        # metadata = s3.head_object(Bucket=Bucket, Key=key)
        # print(metadata['ResponseMetadata']['HTTPHeaders']['content-length'])
        metadata = ffmpeg.probe(video_obj.decode())
        for stream in metadata.streams:
            print(stream)
        return {
                # 'duration': str(timedelta(seconds=int(float(video_info['duration'])))),
                # 'width': video_info['width'],
                # 'height': video_info['height']
                'duration': '00:00:00',
                'width': 1920,
                'height': 1080
            }

    @staticmethod
    def remove_video(track_id, user_id):
        try:
            dir = f"users/{user_id}/videos/{track_id}/"
            bucket = s3.get_bucket(Bucket)
            for obj in bucket.list(prefix=dir):
                obj.delete()

        except Exception as e:
            print('REMOVE VIDEO Error:', e)
            return False
        return True
