from django.db import models

from state.models import StateModel
from django.utils.timezone import now

# Create your models here.
class CityModel(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=50)
    state = models.ForeignKey(StateModel, on_delete=models.CASCADE)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.city_id},{self.city_name})"

    class Meta:
        db_table = "city"

