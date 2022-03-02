from django.db import models
from django.utils.timezone import now

from advice.models import AdviceModel
from diagnosis.models import DiagnosisModel
from patient.models import PatientModel
from patient_opd.models import PatientOpdModel


# Create your models here.
class PatientIndoorModel(models.Model):
    patient_indoor_id = models.AutoField(primary_key=True)
    patient_opd = models.ForeignKey(PatientOpdModel, on_delete=models.DO_NOTHING, null=True)
    patient = models.ForeignKey(PatientModel, on_delete=models.DO_NOTHING)
    regd_no = models.CharField(max_length=100, default="")

    indoor_case_number = models.CharField(max_length=100, default="")
    indoor_date = models.DateField(null=True)
    indoor_time = models.CharField(max_length=15, null=True)
    complain = models.CharField(max_length=500, null=True)
    temprature = models.CharField(max_length=25, default="", null=True)
    pulse = models.FloatField(default=0.0, null=True)
    bp = models.CharField(max_length=25, default="", null=True)
    spo2 = models.CharField(max_length=15, default="", null=True)
    pallor = models.CharField(max_length=25, default="", null=True)
    lcterus = models.CharField(max_length=25, default="", null=True)
    oedema = models.CharField(max_length=25, default="", null=True)
    rs = models.CharField(max_length=25, default="", null=True)
    cvs = models.CharField(max_length=25, default="", null=True)
    pa_gyn = models.CharField(max_length=25, default="", null=True)
    pa_obs = models.CharField(max_length=25, default="", null=True)
    ut_weeks = models.IntegerField(default=0, null=True)
    eb_pp = models.CharField(max_length=25, default="", null=True)
    fhs = models.CharField(max_length=25, default="", null=True)
    ut = models.CharField(max_length=25, default="", null=True)
    ps = models.CharField(max_length=25, default="", null=True)
    pv = models.CharField(max_length=25, default="", null=True)
    ut_contra = models.CharField(max_length=25, default="", null=True)
    adm_date = models.DateField(null=True)
    adm_time = models.CharField(max_length=15, default="", null=True)
    oper_date = models.DateField(null=True)
    oper_time = models.CharField(max_length=15, default="", null=True)
    disch_date = models.DateField(null=True)
    disch_time = models.CharField(max_length=15, default="", null=True)
    operation = models.CharField(max_length=50, default="", null=True)
    diagnosis = models.ForeignKey(DiagnosisModel, on_delete=models.DO_NOTHING, null=True)
    field_order = models.CharField(max_length=25, default="", null=True)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.patient_indoor_id})"

    class Meta:
        db_table = "patient_indoor"


class IndoorAdviceModel(models.Model):
    indoor_advice_id = models.AutoField(primary_key=True)
    patient_indoor = models.ForeignKey(PatientIndoorModel, on_delete=models.CASCADE)

    advice = models.ForeignKey(AdviceModel, on_delete=models.DO_NOTHING)
    advice_date = models.DateField(null=True)
    advice_time = models.CharField(max_length=15, null=True)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.indoor_advice_id})"

    class Meta:
        db_table = "indoor_advice"
