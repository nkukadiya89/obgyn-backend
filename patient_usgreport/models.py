from django.db import models
from django.utils.timezone import now

from patient.models import PatientModel
from patient_opd.models import PatientOpdModel


# Create your models here.
class PatientUSGReportModel(models.Model):
    patient_usgreport_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(PatientModel, on_delete=models.DO_NOTHING)
    patient_opd = models.OneToOneField(PatientOpdModel, on_delete=models.DO_NOTHING)
    regd_no = models.CharField(max_length=100, default="")

    report_date = models.DateField(default=now)
    no_of_foetus = models.IntegerField(default=0)
    cardiac_activity = models.CharField(max_length=100, default="")
    presentation = models.TextField(null=True)
    ga_weeks = models.IntegerField(default=0)
    ga_day = models.IntegerField(default=0)
    ga_edd = models.IntegerField(default=0)
    crl_weeks = models.IntegerField(default=0)
    crl_day = models.IntegerField(default=0)
    crl_edd = models.IntegerField(default=0)
    fl_weeks = models.IntegerField(default=0)
    fl_day = models.IntegerField(default=0)
    fl_edd = models.IntegerField(default=0)
    bpd_weeks = models.IntegerField(default=0)
    bpd_day = models.IntegerField(default=0)
    bpd_edd = models.IntegerField(default=0)
    hc_weeks = models.IntegerField(default=0)
    hc_day = models.IntegerField(default=0)
    hc_edd = models.IntegerField(default=0)
    ac_weeks = models.IntegerField(default=0)
    ac_day = models.IntegerField(default=0)
    ac_edd = models.IntegerField(default=0)
    avg_weeks = models.IntegerField(default=0)
    avg_day = models.IntegerField(default=0)
    avg_edd = models.IntegerField(default=0)
    possible_lmp = models.CharField(max_length=100, default="")
    placental_location = models.CharField(max_length=100, default="")
    amount_of_liquor = models.CharField(max_length=100, default="")
    anomalies = models.CharField(max_length=250, default="")
    remark = models.TextField(null=True)
    usg_report = models.TextField(null=True)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.patient_usgreport_id})"

    class Meta:
        db_table = "patient_usgreport"
