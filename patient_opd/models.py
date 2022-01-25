from django.db import models
from django.utils.timezone import now

from patient.models import PatientModel


# Create your models here.
class PatientOpdModel(models.Model):
    patient_opd_id = models.AutoField(primary_key=True)
    opd_date = models.DateField(default=now)
    regd_no = models.CharField(max_length=100, default="")
    patient = models.ForeignKey(PatientModel, on_delete=models.DO_NOTHING)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.patient_opd_id})"

    class Meta:
        db_table = "patient_opd"
