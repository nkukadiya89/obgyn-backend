from django.db import models
from django.utils.timezone import now

from patient.models import PatientModel
from patient_opd.models import PatientOpdModel
from manage_fields.models import ManageFieldsModel


# Create your models here.
class PatientUSGReportModel(models.Model):
    patient_usgreport_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(PatientModel, on_delete=models.DO_NOTHING)
    patient_opd = models.ForeignKey(PatientOpdModel, on_delete=models.DO_NOTHING)
    regd_no = models.CharField(max_length=100, default="")

    report_date = models.DateField(default=now,null=True)
    no_of_foetus = models.CharField(max_length=25, default="",null=True)
    cardiac_activity = models.CharField(max_length=100, default="",null=True)
    presentation = models.TextField(null=True)
    ga_weeks = models.IntegerField(default=0,null=True)
    ga_day = models.IntegerField(default=0,null=True)
    ga_edd = models.DateField(null=True)
    crl_weeks = models.IntegerField(default=0,null=True)
    crl_day = models.IntegerField(default=0,null=True)
    crl_edd = models.DateField(null=True)
    fl_weeks = models.IntegerField(default=0,null=True)
    fl_day = models.IntegerField(default=0,null=True)
    fl_edd = models.DateField(null=True)
    bpd_weeks = models.IntegerField(default=0,null=True)
    bpd_day = models.IntegerField(default=0,null=True)
    bpd_edd = models.DateField(null=True)
    hc_weeks = models.IntegerField(default=0,null=True)
    hc_day = models.IntegerField(default=0,null=True)
    hc_edd = models.DateField(null=True)
    ac_weeks = models.IntegerField(default=0,null=True)
    ac_day = models.IntegerField(default=0,null=True)
    ac_edd = models.DateField(null=True)
    avg_weeks = models.IntegerField(default=0,null=True)
    avg_day = models.IntegerField(default=0,null=True)
    avg_edd = models.DateField(null=True)
    possible_lmp = models.CharField(max_length=100, default="",null=True)
    placental_location = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="placental_location")
    amount_of_liquor = models.CharField(max_length=100, default="",null=True)
    anomalies = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="anomalies")
    remark = models.TextField(null=True)
    usg_report = models.TextField(null=True)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.patient_usgreport_id})"

    class Meta:
        db_table = "patient_usgreport"
