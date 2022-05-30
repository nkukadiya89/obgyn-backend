from operator import mod
from django.db import models
from user.models import User
from manage_fields.models import FieldMasterModel
from city.models import CityModel
from taluka.models import TalukaModel
from district.models import DistrictModel
from state.models import StateModel

from django.utils.timezone import now

# Create your models here.
class ObgynConfigModel(models.Model):
    obgyn_config_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    rs_per_visit = models.FloatField(default=0, null=True)
    rs_per_usg = models.FloatField(default=0, null=True)
    rs_per_room = models.FloatField(default=0, null=True)
    operative_charge = models.FloatField(default=0, null=True)
    rs_per_day_nursing = models.FloatField(default=0, null=True)
    field_master_name  = models.ForeignKey(FieldMasterModel, on_delete=models.DO_NOTHING, null=True)
    city = models.ForeignKey(CityModel, on_delete=models.CASCADE, null=True)
    taluka = models.ForeignKey(TalukaModel, on_delete=models.CASCADE, null=True)
    district = models.ForeignKey(DistrictModel, on_delete=models.CASCADE, null=True)
    state = models.ForeignKey(StateModel, on_delete=models.CASCADE, null=True)
    monthly_usg = models.IntegerField(default=0,null=True)
    yearly_usg = models.IntegerField(default=0,null=True)
    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    class Meta:
        db_table = "obgyn_config"