from django.db import models
from django.utils.timezone import now

from medicine.models import MedicineModel


# Create your models here.
class DiagnosisModel(models.Model):
    diagnosis_id = models.AutoField(primary_key=True)
    diagnosis_name = models.CharField(max_length=150, default="")
    medicine = models.ManyToManyField(MedicineModel)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.diagnosis_id},{self.diagnosis_name})"

    class Meta:
        db_table = "diagnosis"
