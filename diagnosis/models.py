from django.db import models
from django.utils.timezone import now

from medicine.models import MedicineModel


# Create your models here.
class DiagnosisModel(models.Model):
    diagnosisId = models.AutoField(primary_key=True)
    diagnosisName = models.CharField(max_length=150, default="")
    medicine = models.ManyToManyField(MedicineModel)

    createdBy = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    createdAt = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.diagnosisId},{self.diagnosisName})"

    class Meta:
        db_table = "diagnosis"

