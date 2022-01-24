from django.db import models
from django.utils.timezone import now

from consultation.models import ConsultationModel
from patient.models import PatientModel
from diagnosis.models import DiagnosisModel


# Create your models here.
class PatientPrescriptionModel(models.Model):
    patient_prescription_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(PatientModel, on_delete=models.DO_NOTHING, null=True)
    regd_no = models.CharField(max_length=100, default="")
    consultation = models.ForeignKey(ConsultationModel, on_delete=models.DO_NOTHING, null=True)
    diagnosis = models.ForeignKey(DiagnosisModel, on_delete=models.DO_NOTHING, null=True)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.patient_prescription_id})"

    class Meta:
        db_table = "patient_prescription"
