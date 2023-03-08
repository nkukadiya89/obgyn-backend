from django.contrib import admin
from city.models import CityModel
from district.models import DistrictModel
from taluka.models import TalukaModel
# Register your models here.
admin.site.register(CityModel)
admin.site.register(DistrictModel)
admin.site.register(TalukaModel)