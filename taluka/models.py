from django.db import models

from district.models import DistrictModel
from django.utils.timezone import now

# Create your models here.
class TalukaModel(models.Model):
    taluka_id = models.AutoField(primary_key=True)
    taluka_name = models.CharField(max_length=50)
    district = models.ForeignKey(DistrictModel, on_delete=models.CASCADE)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.taluka_id},{self.taluka_name})"

    class Meta:
        db_table = "taluka"

