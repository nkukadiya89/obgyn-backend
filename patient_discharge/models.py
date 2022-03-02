from django.db import models
from django.utils.timezone import now
from patient.models import PatientModel
from patient_opd.models import PatientOpdModel
from diagnosis.models import DiagnosisModel
from advice.models import AdviceModel
from manage_fields.models import ManageFieldsModel

# Create your models here.
class PatientDischargeModel(models.Model):
    patient_discharge_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(PatientModel, on_delete=models.DO_NOTHING)
    patient_opd = models.OneToOneField(PatientOpdModel, on_delete=models.DO_NOTHING)
    regd_no = models.CharField(max_length=100, default="")

    admission_date = models.DateField(default=now)
    admission_time = models.CharField(max_length=15, default="")
    complain_of = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="complain_of")
    diagnosis = models.ForeignKey(DiagnosisModel, on_delete=models.DO_NOTHING)
    name_of_operation = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="name_of_operation")
    ot_date = models.DateField(default=now)
    ot_time = models.CharField(max_length=15, default="")
    treatment_given = models.CharField(max_length=250, default="")
    advice = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="pd_advice")
    any_history = models.TextField(null=True)
    assisted = models.CharField(max_length=250, default="")
    discharge_date = models.DateField(default=now)
    discharge_time = models.CharField(max_length=15, default="")
    remark = models.TextField(null=True)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.patient_discharge_id})"

    class Meta:
        db_table = "patient_discharge"
