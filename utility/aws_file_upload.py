from os import path, remove
from os.path import isfile
from urllib.parse import urlparse

import boto3
from PIL import Image
from decouple import config
from django.conf import settings
from django.utils import timezone
from rest_framework import serializers
# from barcode import  EAN13
import barcode
from barcode.writer import ImageWriter
import os


ACCESS_KEY = config("AWS_ACCESS_KEY")
SECRET_KEY = config("AWS_SECRET_KEY")
REGION_NAME = config("REGION_NAME")
BUCKET = config("BUCKET_NAME")


def get_bucket_file_folder(aws_file_url):
    o = urlparse(aws_file_url, allow_fragments=False)
    return o.path.lstrip("/")


def file_extention(file_path):
    return path.splitext(file_path)[1]


def upload_file_to_bucket(
    upload_file, allowed_type, folder_name, p_value, file_name=None
):
    file_type = file_extention(str(upload_file))

    if file_type not in allowed_type:
        return serializers.ValidationError("File Type not supported")

    s3 = boto3.client(
        "s3",
        region_name=REGION_NAME,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )

    if file_name == None:
        file_name = timezone.now().strftime("%Y%m%d-%H%M%S")

    file_to_upload = Image.open(upload_file)
    picture_format = "image/" + file_to_upload.format.lower()

    tempfile = settings.MEDIA_ROOT + file_name + file_type
    file_to_upload.save(tempfile)

    s3_file = f"{folder_name}" + str(p_value) + "_" + file_name + file_type

    aws_file_url = f"http://{BUCKET}.s3.{REGION_NAME}.amazonaws.com/{s3_file}"

    s3.upload_file(
        tempfile,
        BUCKET,
        s3_file,
        ExtraArgs={"ACL": "public-read", "ContentType": picture_format},
    )

    presigned_url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET, "Key": get_bucket_file_folder(aws_file_url)},
        ExpiresIn=300,
    )

    isfile(tempfile)
    remove(tempfile)
    return aws_file_url, presigned_url


def upload_barcode_image(regd_no, mobile_no, patient_id):
   
    EAN = barcode.get_barcode_class('code128')
    my_code = EAN(regd_no, writer=ImageWriter())
    directory = "static/barcode/" + str(patient_id)
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = my_code.save(directory + "/" + regd_no)
    regd_no_barcode_url, presigned_url = upload_file_to_bucket(
        filename, ".png", "barcode/"+str(patient_id) + "/", patient_id, "regd_no"
    )

    isfile(filename)
    remove(filename)

    print(mobile_no)
    my_code =  EAN(mobile_no, writer=ImageWriter())
    directory = "static/barcode/" + str(patient_id)
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = my_code.save(directory + "/" + mobile_no)
    mobile_no_barcode_url, presigned_url = upload_file_to_bucket(
        filename, ".png", "barcode/"+str(patient_id) + "/", patient_id, "mobile_no"
    )

    isfile(filename)
    remove(filename)


    return regd_no_barcode_url,mobile_no_barcode_url
