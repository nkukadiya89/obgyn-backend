from django.db import models
from user.models import User
from django.utils.timezone import now

# Create your models here.
class PatientModel(User):
    department_choice = (
        ("OPD", "OPD"),
        ("IPD", "IPD")
    )
    patient_type_choice = (
        ("OB", "OB"),
        ("GYN", "GYN")
    )
    patient_detail_choice = (
        ("FULL", "FULL"),
        ("PARTIAL", "PARTIAL")
    )
    patient_id = models.AutoField(primary_key=True)
    married = models.BooleanField(default=False)
    department = models.CharField(max_length=5, choices=department_choice, default="OPD")
    patient_type = models.CharField(max_length=5, choices=patient_type_choice, default="OB")
    patient_detail = models.CharField(max_length=8,choices=patient_detail_choice, default="PARTIAL")
    date_of_opd = models.DateField(default=now)
    registered_no = models.CharField(max_length=100, default="")
    husband_father_name = models.CharField(max_length=100, default="")
    grand_father_name = models.CharField(max_length=100, default="")
    age = models.IntegerField(default=0)
    taluka = models.CharField(max_length=100, default="")
    district = models.CharField(max_length=100, default="")

    class Meta:
        db_table = 'patient'
