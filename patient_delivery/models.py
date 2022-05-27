from django.db import models
from django.utils.timezone import now

from patient.models import PatientModel


# Create your models here.
class PatientDeliveryModel(models.Model):
    gender_choice = (
        ("MALE", "MALE"),
        ("FEMALE", "FEMALE")
    )
    delivery_type_choice = (
        ("NORMAL", "NORMAL"),
        ("CESARIAN", "CESARIAN")
    )

    patient_delivery_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(PatientModel, on_delete=models.DO_NOTHING)
    regd_no = models.CharField(max_length=100, default="")

    baby_no = models.IntegerField(default=0, null=True)
    sr_no = models.CharField(max_length=50, default="")
    birth_date = models.DateField(null=True)
    birth_time = models.CharField(max_length=10, null=True)
    husband_name = models.CharField(max_length=50, null=True)
    child_name = models.CharField(max_length=100, default="")
    child_gender = models.CharField(max_length=10, choices=gender_choice, default="MALE")
    delivery_type = models.CharField(max_length=10, choices=delivery_type_choice, default="NORMAL")
    religion = models.CharField(max_length=25, default="")
    episio_by = models.CharField(max_length=100, default="")
    dayan = models.CharField(max_length=100, default="")
    village = models.CharField(max_length=100, default="")
    taluka = models.CharField(max_length=100, default="")
    district = models.CharField(max_length=100, default="")
    pin = models.IntegerField(null=True)
    marriage_age = models.IntegerField(default=0, null=True)
    current_age = models.IntegerField(default=0, null=True)
    weeks = models.IntegerField(default=0, null=True)
    live_male_female = models.IntegerField(default=0, null=True)
    no_of_delivery = models.IntegerField(default=0, null=True)
    weight = models.FloatField(default=0.0, null=True)
    father_education = models.CharField(max_length=100, default="")
    mother_education = models.CharField(max_length=100, default="")
    father_occupation = models.CharField(max_length=250, default="")
    mother_occupation = models.CharField(max_length=250, default="")
    baby_status = models.CharField(max_length=15, default="")
    serial_no_month = models.IntegerField(default=0, null=True)
    serial_no_year = models.IntegerField(default=0, null=True)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.patient_delivery_id},{self.child_name})"

    class Meta:
        db_table = "patient_delivery"
