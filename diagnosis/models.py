from django.db import models
from django.utils.timezone import now

from medicine.models import MedicineModel


# Create your models here.
class DiagnosisModel(models.Model):
    diagnosis_id = models.AutoField(primary_key=True)
    diagnosis_name = models.CharField(max_length=150, default="", null=True)
    diagnosis_type = models.CharField(max_length=3, default="D")
    medicine = models.ManyToManyField(MedicineModel)
    ut_weeks = models.IntegerField(null=True)
    ut_days = models.IntegerField(null=True)
    advice = models.CharField(max_length=100, null=True)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.diagnosis_id},{self.diagnosis_name})"

    class Meta:
        db_table = "diagnosis"


class DiagnosisMedicineModel(models.Model):
    diagnosismodel = models.ForeignKey(DiagnosisModel, on_delete=models.DO_NOTHING)
    medicinemodel = models.ForeignKey(MedicineModel, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "diagnosis_medicine"
        managed = False
