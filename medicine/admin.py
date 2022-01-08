from django.contrib import admin
from medicine.models import MedicineModel,MedicineTypeModel,TimingModel

# Register your models here.
admin.site.register(MedicineModel)
admin.site.register(MedicineTypeModel)
admin.site.register(TimingModel)