from django.db import models
from django.utils.timezone import now

from language.models import LanguageModel


# Create your models here.
class MedicineTypeModel(models.Model):
    medicineTypeId = models.AutoField(primary_key=True)
    medicineType = models.CharField(max_length=50, default="")

    createdBy = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    createdAt = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.medicineTypeId},{self.medicineType})"

    class Meta:
        db_table = "medicine_type"


class TimingModel(models.Model):
    timingId = models.AutoField(primary_key=True)
    language = models.ForeignKey(LanguageModel, on_delete=models.SET_NULL, null=True, db_column="languageId")
    timing = models.CharField(max_length=25, default="")

    createdBy = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    createdAt = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.timingId},{self.timing})"

    class Meta:
        db_table = "timing"


class MedicineModel(models.Model):
    medicineId = models.AutoField(primary_key=True)
    barcode = models.CharField(max_length=20, default="")
    medicineType = models.ForeignKey(MedicineTypeModel, on_delete=models.SET_NULL, null=True,
                                     db_column="medicineTypeId")
    medicine = models.CharField(max_length=250, default="")
    contain = models.CharField(max_length=500, default="")
    perDay = models.IntegerField(default=0)
    forDay = models.IntegerField(default=0)
    totalTablet = models.IntegerField(default=0)
    company = models.CharField(max_length=250, default="")
    morningTiming = models.ForeignKey(TimingModel, on_delete=models.SET_NULL, null=True, related_name="morning_timing",
                                      db_column="morningTimingId")
    noonTiming = models.ForeignKey(TimingModel, on_delete=models.SET_NULL, null=True, related_name="noon_timing",
                                   db_column="noonTimingId")
    eveningTiming = models.ForeignKey(TimingModel, on_delete=models.SET_NULL, null=True, related_name="evening_timing",
                                      db_column="eveningTimingId")
    bedTiming = models.ForeignKey(TimingModel, on_delete=models.SET_NULL, null=True, related_name="bed_timing",
                                  db_column="bedTimingId")

    createdBy = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    createdAt = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.medicineId},{self.medicine})"

    class Meta:
        db_table = "medicine"
