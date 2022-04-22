from os import path,remove
from os.path import isfile
from urllib.parse import urlparse

import boto3
from PIL import Image
from decouple import config
from django.conf import settings
from django.utils import timezone
from rest_framework import serializers

ACCESS_KEY = config('AWS_ACCESS_KEY')
SECRET_KEY = config('AWS_SECRET_KEY')
REGION_NAME = config('REGION_NAME')
BUCKET = config('BUCKET_NAME')


def get_bucket_file_folder(aws_file_url):
    o = urlparse(aws_file_url, allow_fragments=False)
    return o.path.lstrip('/')


def file_extention(file_path):
    return path.splitext(file_path)[1]


def upload_file_to_bucket(upload_file, allowed_type, folder_name, p_value, file_name=None):
    file_type = file_extention(str(upload_file))

    if file_type not in allowed_type:
        return serializers.ValidationError("File Type not supported")

    s3 = boto3.client('s3', region_name=REGION_NAME, aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    if file_name == None:
        file_name = timezone.now().strftime("%Y%m%d-%H%M%S")

    file_to_upload = Image.open(upload_file)
    picture_format = 'image/' + file_to_upload.format.lower()

    tempfile = settings.MEDIA_ROOT + file_name + file_type
    file_to_upload.save(tempfile)

    s3_file = f"{folder_name}" + str(p_value) + "_" + file_name + file_type

    aws_file_url = f"http://{BUCKET}.s3.{REGION_NAME}.amazonaws.com/{s3_file}"

    s3.upload_file(tempfile, BUCKET, s3_file,
                   ExtraArgs={'ACL': 'public-read', 'ContentType': picture_format})

    presigned_url = s3.generate_presigned_url('get_object', Params={'Bucket': BUCKET,
                                                                    'Key': get_bucket_file_folder(
                                                                        aws_file_url)}, ExpiresIn=300)

    isfile(tempfile)
    remove(tempfile)
    return aws_file_url, presigned_url
