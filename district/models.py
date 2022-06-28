from operator import mod
from re import T
from django.db import models
from language.models import LanguageModel

from state.models import StateModel
from django.utils.timezone import now
from language.models import LanguageModel

# Create your models here.
class DistrictModel(models.Model):
    district_id = models.AutoField(primary_key=True)
    district_name = models.CharField(max_length=50)
    state = models.ForeignKey(StateModel, on_delete=models.CASCADE)
    language = models.ForeignKey(LanguageModel,on_delete=models.DO_NOTHING, null=True)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.district_id},{self.district_name})"

    class Meta:
        db_table = "district"

