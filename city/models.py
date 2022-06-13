from re import T
from django.db import models

from taluka.models import TalukaModel
from django.utils.timezone import now
from language.models import LanguageModel

# Create your models here.
class CityModel(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=50)
    taluka = models.ForeignKey(TalukaModel, on_delete=models.CASCADE, null=True)
    language = models.ForeignKey(LanguageModel,on_delete=models.DO_NOTHING, null=True)
    

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.city_id},{self.city_name})"

    class Meta:
        db_table = "city"

