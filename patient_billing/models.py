from django.db import models
from django.utils.timezone import now

from diagnosis.models import DiagnosisModel
from patient.models import PatientModel
from patient_opd.models import PatientOpdModel


# Create your models here.
class PatientBillingModel(models.Model):
    patient_billing_id = models.AutoField(primary_key=True)
    patient_opd = models.ForeignKey(PatientOpdModel, on_delete=models.DO_NOTHING, null=True)
    patient = models.ForeignKey(PatientModel, on_delete=models.DO_NOTHING)
    regd_no = models.CharField(max_length=100, default="")

    invoice_no = models.CharField(max_length=25, null=True)
    admission_date = models.DateField(null=True)
    ot_date = models.DateField(null=True)
    discharge_date = models.DateField(null=True)
    diagnosis = models.ForeignKey(DiagnosisModel, on_delete=models.DO_NOTHING)
    procedure_name = models.CharField(max_length=100, null=True)
    no_of_visit = models.IntegerField(default=0)
    rs_per_visit = models.FloatField(default=0.0)
    consulting_fees = models.FloatField(default=0.0)
    no_of_usg = models.IntegerField(default=0)
    rs_per_usg = models.FloatField(default=0.0)
    usg_rs = models.FloatField(default=0.0)
    room_no_of_day = models.CharField(max_length=25, null=True)
    rs_per_room = models.FloatField(default=0.0)
    room_type = models.CharField(max_length=25, default="")
    room_rs = models.FloatField(default=0.0)
    operative_charge_rs = models.FloatField(default=0.0)
    medicine_rs = models.FloatField(default=0.0)
    nursing_no_of_days = models.IntegerField(default=0)
    rs_per_day = models.FloatField(default=0.0)
    nursing_rs = models.FloatField(default=0.0)
    other_charge = models.FloatField(default=0.0)
    other_rs = models.FloatField(default=0.0)
    total_rs = models.FloatField(default=0.0)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.patient_billing_id})"

    class Meta:
        db_table = "patient_billing"
