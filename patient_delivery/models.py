from operator import mod
from pyexpat import model
from django.db import models
from django.utils.timezone import now

from patient.models import PatientModel
from city.models import CityModel
from taluka.models import TalukaModel
from district.models import DistrictModel
from state.models import StateModel
from manage_fields.models import ManageFieldsModel


# Create your models here.
class PatientDeliveryModel(models.Model):
    gender_choice = (
        ("MALE", "MALE"),
        ("FEMALE", "FEMALE"),
        ("OTHER", "OTHER")
    )
    delivery_type_choice = (
        ("NORMAL", "NORMAL"),
        ("CESARIAN", "CESARIAN"),
        ("INSTRUMENTAL","INSTRUMENTAL"),
    )

    patient_delivery_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(PatientModel, on_delete=models.DO_NOTHING)
    regd_no = models.CharField(max_length=100, default="")

    baby_no = models.CharField(max_length=35, null=True)
    sr_no = models.IntegerField(null=True)
    birth_date = models.DateField(null=True)
    birth_time = models.CharField(max_length=10, null=True)
    husband_name = models.CharField(max_length=50, null=True)
    mother_name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150, null=True)
    husband_father_name = models.CharField(max_length=150, null=True)
    child_name = models.CharField(max_length=100, default="")
    child_gender = models.CharField(max_length=10, choices=gender_choice, default="MALE")
    delivery_type = models.CharField(max_length=20, choices=delivery_type_choice, default="NORMAL")
    religion = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, related_name="delivery_religion", null=True)
    episio_by = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, related_name="delivery_dpisio_by", null=True)
    dayan = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, related_name="delivery_dayan", null=True)
    city = models.ForeignKey(CityModel,on_delete=models.DO_NOTHING, null=True)
    taluka = models.ForeignKey(TalukaModel,on_delete=models.DO_NOTHING, null=True)
    district = models.ForeignKey(DistrictModel,on_delete=models.DO_NOTHING, null=True)
    state = models.ForeignKey(StateModel,on_delete=models.DO_NOTHING, null=True)
    pin = models.IntegerField(null=True)
    landmark = models.CharField(max_length=500, null=True)
    lastname = models.CharField(max_length=100, null=True)
    marriage_age = models.IntegerField(default=0, null=True)
    current_age = models.IntegerField(default=0, null=True)
    weeks = models.IntegerField(default=0, null=True)
    live_male_female = models.CharField(max_length=15, null=True)
    no_of_delivery = models.IntegerField(default=0, null=True)
    weight = models.FloatField(default=0.0, null=True)
    father_education = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, related_name="delivery_f_education", null=True)
    mother_education = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, related_name="delivery_m_education", null=True)
    father_occupation = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, related_name="delivery_f_occupation", null=True)
    mother_occupation = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, related_name="delivery_m_occupation", null=True)
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
