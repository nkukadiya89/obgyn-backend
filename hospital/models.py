from user.models import User
from django.db import models


from city.models import CityModel
from language.models import LanguageModel
from state.models import StateModel
from django.utils.timezone import now


# Create your models here.
class HospitalModel(models.Model):
    hospital_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    hospital_name = models.CharField(max_length=250)
    state = models.ForeignKey(StateModel, on_delete=models.DO_NOTHING, null=True)
    city = models.ForeignKey(CityModel, on_delete=models.DO_NOTHING, null=True)
    area = models.CharField(max_length=250)
    pincode = models.CharField(max_length=20)
    default_language = models.ForeignKey(LanguageModel, on_delete=models.DO_NOTHING)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.hospital_name},{self.city})"

    class Meta:
        db_table = "hospital"
