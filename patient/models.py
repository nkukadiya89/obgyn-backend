import os
from urllib.parse import urlparse
from django.db.models.query import Q
from django.db.models.signals import post_save
from decouple import config
from django.db import models
from django.utils.timezone import now
from manage_fields.models import ManageFieldsModel

from user.models import User
from utility.aws_file_upload import upload_file_to_bucket

ACCESS_KEY = config('AWS_ACCESS_KEY')
SECRET_KEY = config('AWS_SECRET_KEY')
REGION_NAME = config('REGION_NAME')
BUCKET = config('BUCKET_NAME')


# Create your models here.
class PatientModel(User):
    gender_choice =(
        ("MALE","MALE"),
        ("FEMALE","FEMALE"),
        ('TRANSGENDER','TRANSGENDER')
    )
    patient_id = models.AutoField(primary_key=True)
    name_title = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, related_name="name_title", null=True)
    married = models.BooleanField(default=False)
    profile_image = models.CharField(max_length=250, default="", null=True)
    date_of_opd = models.DateField(default=now)
    registered_no = models.CharField(max_length=100, default="")
    husband_father_name = models.CharField(max_length=100, default="",null=True) 
    husband_title = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, related_name="husband_title",
                                      null=True)
    grand_father_name = models.CharField(max_length=100, default="",null=True)
    grand_title = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, related_name="grand_title",
                                    null=True)

    regd_no_barcode = models.CharField(max_length=250, null=True)
    mob_no_barcode = models.CharField(max_length=250, null=True)

    age = models.IntegerField(default=0,null=True)
    
    religion = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, related_name="religion",
                                      null=True)
    first_edd = models.DateField(null=True)
    gender = models.CharField(max_length=15, choices=gender_choice, default="FEMALE")

    class Meta:
        db_table = 'patient'

    def upload_file(self, file_to_upload):
        allowed_type = [".jpg", ".png", ".jpeg"]
        file_name = "profile_image"
        self.profile_image, presigned_url = upload_file_to_bucket(file_to_upload, allowed_type, "patient/", self.patient_id,file_name)


def get_bucket_file_folder(aws_file_url):
    o = urlparse(aws_file_url, allow_fragments=False)
    return o.path.lstrip('/')


def file_extention(path):
    return os.path.splitext(path)[1]


def user_post_save(sender, instance, *args, **kwargs):
    if kwargs["created"]:
        seq_no = 0
        last_user = User.objects.filter(user_type=instance.user_type).filter(~Q(pk=instance.id)).last()

        if last_user:
            seq_no = int(last_user.user_code[-4:])
            seq_no += 1

        instance.user_code = instance.user_type[0] + '{:05}'.format(seq_no)
        instance.save()


post_save.connect(user_post_save, sender=PatientModel)
