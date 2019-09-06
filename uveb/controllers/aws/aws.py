import boto3
import ffmpeg

from uveb import app


s3 = boto3.client('s3',
                  aws_access_key_id=app.config['AWS_ACCESS_KEY'],
                  aws_secret_access_key=app.config['AWS_SECRET_KEY'])
resource = boto3.resource('s3',
                          aws_access_key_id=app.config['AWS_ACCESS_KEY'],
                          aws_secret_access_key=app.config['AWS_SECRET_KEY'])
Main_Bucket = app.config['MAIN_BUCKET']
Temp_Bucket = app.config['TEMP_BUCKET']


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
            key = f'uploads/images/original{user_id}.' + ext
            s3.upload_fileobj(
                img_obj,
                Temp_Bucket,
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
    def upload_video(video_obj, track_id):
        try:
            ext = video_obj.filename.split('.')[1]
            key = 'uploads/videos/' + track_id + '.' + ext
            s3.upload_fileobj(
                video_obj,
                Temp_Bucket,
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
    def get_video_info(key):
        metadata = ffmpeg.probe(app.config['TEMP_STORE_PATH'] + key)
        obj = resource.Object(Temp_Bucket, key)
        file_size = obj.content_length
        return {
                'duration': int(metadata['streams'][0]['duration']),
                'width': int(metadata['streams'][0]['width']),
                'height': int(metadata['streams'][0]['height']),
                'size': file_size
            }

    @staticmethod
    def cancel_video_upload(key):
        try:
            print(key)
            resource.Object(Temp_Bucket, key).delete()

        except Exception as e:
            print('CANCEL VIDEO UPLOAD Error:', e)
            return False
        return True

    @staticmethod
    def remove_one_video(prefix):
        try:
            bucket = resource.Bucket(Main_Bucket)
            bucket.objects.filter(Prefix=prefix).delete()

        except Exception as e:
            print('REMOVE ONE VIDEO Error:', e)
            return False
        return True
