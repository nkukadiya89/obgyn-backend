from django.db import models

from state.models import StateModel
from django.utils.timezone import now

# Create your models here.
class CityModel(models.Model):
    cityId = models.AutoField(primary_key=True)
    cityName = models.CharField(max_length=50)
    state = models.ForeignKey(StateModel, on_delete=models.CASCADE, db_column="stateId", related_name="stateID")

    createdBy = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    createdAt = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.cityId},{self.cityName})"

    class Meta:
        db_table = "city"
