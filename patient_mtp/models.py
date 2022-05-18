from django.db import models
from django.utils.timezone import now

from patient.models import PatientModel
from patient_opd.models import PatientOpdModel
from manage_fields.models import ManageFieldsModel

# Create your models here.
class PatientMtpModel(models.Model):
    patient_mtp_id = models.AutoField(primary_key=True)
    patient_opd = models.ForeignKey(PatientOpdModel, on_delete=models.DO_NOTHING, null=True)
    patient = models.ForeignKey(PatientModel, on_delete=models.DO_NOTHING)
    regd_no = models.CharField(max_length=100, default="")

    second_rmp = models.CharField(max_length=25, null=True)
    admission_date = models.DateField(null=True)
    admission_time = models.CharField(max_length=10, null=True)
    procedure_date = models.DateField(null=True)
    procedure_time = models.CharField(max_length=10, null=True)
    reason_for_mtp = models.CharField(max_length=250, null=True)
    contraception = models.CharField(max_length=100, null=True)
    mtp_complication = models.CharField(max_length=500, null=True)
    termination_date = models.DateField(null=True)
    discharge_date = models.DateField(null=True)
    discharge_time = models.CharField(max_length=10, null=True)
    remark = models.TextField(null=True)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.patient_mtp_id})"

    class Meta:
        db_table = "patient_mtp"
