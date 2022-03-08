from django.db import models
from django.utils.timezone import now

from patient.models import PatientModel


# Create your models here.
class PatientOpdModel(models.Model):
    patient_type_choice = (
        ("OB", "OB"),
        ("GYN", "GYN")
    )

    patient_opd_id = models.AutoField(primary_key=True)
    opd_date = models.DateField(default=now)
    opd_time = models.CharField(max_length=10, default="")
    regd_no = models.CharField(max_length=100, default="")
    patient = models.ForeignKey(PatientModel, on_delete=models.DO_NOTHING)
    status = models.BooleanField(default=False,
                                 null=True)  # This will be enable when any examination table gets entry of particular patient
    patient_type = models.CharField(max_length=5, choices=patient_type_choice, default="OB", null=True)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.patient_opd_id})"

    class Meta:
        db_table = "patient_opd"
