import oss2
from oss2.models import PartInfo
import ffmpeg

from uveb import app


endpoint = app.config['ALI_ENDPOINT']
bucket_name = app.config['MAIN_BUCKET']
auth = oss2.Auth(app.config['ALI_ACCESS_KEY'], app.config['ALI_SECRET_KEY'])
bucket = oss2.Bucket(auth, endpoint, bucket_name)


class AliCloudService:
    @staticmethod
    def is_ext_allowed(ext, file_type):
        if file_type == 'image':
            return True if ext in app.config['IMAGE_EXTENSIONS_ALLOWED'] else False

        elif file_type == 'video':
            return True if ext in app.config['VIDEO_EXTENSIONS_ALLOWED'] else False

        else:
            return False

    @staticmethod
    def upload_profile(imageobj, objkey):
        try:
            bucket.put_object(objkey, imageobj)
            return True

        except Exception as e:
            print('<AliCloudService.upload_profile> Error:', e)
            return False

    @staticmethod
    def upload_video(videoobj, objkey):
        try:
            bucket.put_object(objkey, videoobj)
            return True

        except Exception as e:
            print('<AliCloudService.upload_video> Error:', e)
            return False

    @staticmethod
    def get_video_info(objkey):
        try:
            simplifiedmeta = bucket.get_object_meta(objkey)
            url = f'https://{bucket_name}.{endpoint}/{objkey}'
            metadata = ffmpeg.probe(url)
            size = simplifiedmeta.content_length
            return {
                'duration': float(metadata['streams'][0]['duration']),
                'width': int(metadata['streams'][0]['width']),
                'height': int(metadata['streams'][0]['height']),
                'size': size
            }

        except Exception as e:
            print('<AliCloudService.get_video_info> Error:', e)
            return {}

    @staticmethod
    def copy_obj(src_obj, dst_obj):
        try:
            total_size = bucket.head_object(src_obj).content_length
            if total_size < 1000 * 1000 * 1024:
                bucket.copy_object(bucket_name, src_obj, dst_obj)

            else:
                part_size = oss2.determine_part_size(total_size, preferred_size=100 * 1024)
                upload_id = bucket.init_multipart_upload(dst_obj).upload_id
                parts = []

                part_number = 1
                offset = 0
                while offset < total_size:
                    num_to_upload = min(part_size, total_size - offset)
                    byte_range = (offset, offset + num_to_upload - 1)

                    result = bucket.upload_part_copy(bucket.bucket_name, src_obj, byte_range, dst_obj, upload_id,
                                                     part_number)
                    parts.append(PartInfo(part_number, result.etag))

                    offset += num_to_upload
                    part_number += 1

                bucket.complete_multipart_upload(dst_obj, upload_id, parts)

            return True

        except Exception as e:
            print('<AliCloudService.copy_obj> Error:', e)
            return False

    @staticmethod
    def remove_obj(objkey):
        try:
            bucket.delete_object(objkey)
            return True

        except Exception as e:
            print('<AliCloudService.remove_obj> Error:', e)
            return False

    @staticmethod
    def remove_objs(prefix):
        try:
            obj_list = []
            for obj in oss2.ObjectIterator(bucket, prefix=prefix):
                obj_list.append(obj.key)

            bucket.batch_delete_objects(obj_list)
            return True

        except Exception as e:
            print('<AliCloudService.remove_objs> Error:', e)
            return False









