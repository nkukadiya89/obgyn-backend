from django.db import models

from state.models import StateModel
from django.utils.timezone import now

from django.db.models.signals import post_save,pre_save

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

# def city_post_save(*args,**kwargs):
#     print("Post Save")
#     print(args)
#     print(kwargs)
#
# post_save.connect(city_post_save,sender=CityModel)
#
# def city_pre_save(*args,**kwargs):
#     print("Pre Save")
#     print(args)
#     print(kwargs)
#
# pre_save.connect(city_pre_save,sender=CityModel)