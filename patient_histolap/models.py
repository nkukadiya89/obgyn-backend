from django.db import models
from django.utils.timezone import now

from patient.models import PatientModel
from patient_opd.models import PatientOpdModel
from manage_fields.models import ManageFieldsModel

# Create your models here.
class PatientHistolapModel(models.Model):
    patient_histolap_id = models.AutoField(primary_key=True)
    patient_opd = models.OneToOneField(PatientOpdModel, on_delete=models.DO_NOTHING, null=True)
    patient = models.ForeignKey(PatientModel, on_delete=models.DO_NOTHING)
    regd_no = models.CharField(max_length=100, default="")

    admission_date = models.DateField(null=True)
    admission_time = models.CharField(max_length=10, null=True)
    procedure_date = models.DateField(null=True)
    procedure_time = models.CharField(max_length=10, null=True)
    procedure_name = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="procedure_name")
    right_tube = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="right_tube")
    left_tube = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="left_tube")
    uterus = models.CharField(max_length=100, null=True)
    pod = models.CharField(max_length=100, null=True)
    endo_cavity = models.CharField(max_length=100, null=True)
    cervical_canal = models.CharField(max_length=100, null=True)
    discharge_date = models.DateField(null=True)
    discharge_time = models.CharField(max_length=10, null=True)
    remark = models.TextField(null=True)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.patient_histolap_id})"

    class Meta:
        db_table = "patient_histolap"
