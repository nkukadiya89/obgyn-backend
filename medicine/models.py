from django.db import models
from django.utils.timezone import now

from language.models import LanguageModel


# Create your models here.
class MedicineTypeModel(models.Model):
    medicine_type_id = models.AutoField(primary_key=True)
    medicine_type = models.CharField(max_length=50, default="")

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.medicine_type_id},{self.medicine_type})"

    class Meta:
        db_table = "medicine_type"


class TimingModel(models.Model):
    timing_id = models.AutoField(primary_key=True)
    language = models.ForeignKey(LanguageModel, on_delete=models.SET_NULL, null=True)
    timing = models.CharField(max_length=25, default="")

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.timing_id},{self.timing})"

    class Meta:
        db_table = "timing"


class MedicineModel(models.Model):
    medicine_id = models.AutoField(primary_key=True)
    barcode = models.CharField(max_length=20, default="")
    medicine_type = models.ForeignKey(MedicineTypeModel, on_delete=models.SET_NULL, null=True)
    medicine = models.CharField(max_length=250, default="")
    contain = models.CharField(max_length=500, default="")
    per_day = models.IntegerField(default=0)
    for_day = models.IntegerField(default=0)
    total_tablet = models.IntegerField(default=0)
    company = models.CharField(max_length=250, default="")
    morning_timing = models.ForeignKey(TimingModel, on_delete=models.SET_NULL, null=True, related_name="morning_timing")
    noon_timing = models.ForeignKey(TimingModel, on_delete=models.SET_NULL, null=True, related_name="noon_timing")
    evening_timing = models.ForeignKey(TimingModel, on_delete=models.SET_NULL, null=True, related_name="evening_timing")
    bed_timing = models.ForeignKey(TimingModel, on_delete=models.SET_NULL, null=True, related_name="bed_timing")

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.medicine_id},{self.medicine})"

    class Meta:
        db_table = "medicine"
