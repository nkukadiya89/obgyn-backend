from django.db import models
from django.utils.timezone import now

from manage_fields.models import ManageFieldsModel
from patient.models import PatientModel
from patient_opd.models import PatientOpdModel


# Create your models here.
class PatientOvulationProfileModel(models.Model):
    patient_ovulation_profile_id = models.AutoField(primary_key=True)
    patient_opd = models.ForeignKey(PatientOpdModel, on_delete=models.DO_NOTHING, null=True)
    patient = models.ForeignKey(PatientModel, on_delete=models.DO_NOTHING)
    regd_no = models.CharField(max_length=100, default="")

    op_day = models.CharField(max_length=10, default="")
    op_date = models.DateField(null=True)
    ut_blood_flow = models.CharField(max_length=100, default="")
    ovarian_blood_flow = models.CharField(max_length=100, default="")
    right_ovary_mm = models.FloatField(default=0.0)
    left_ovary_mm = models.FloatField(default=0.0)
    endometrium_mm = models.FloatField(default=0.0)
    remark = models.TextField(null=True)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.patient_ovulation_profile_id})"

    class Meta:
        db_table = "patient_ovulation_profile"
