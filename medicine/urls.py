from django.urls import path

from .views import (
    MedicineAPI,
    MedicineTypeAPI,
    TimingAPI,
    delete_medicine_type,
    delete_timing,
    patch_medicine,
    patch_timing,
    patch_medicine_type,
    get_medicine,
    get_or_medicine,
    get_medicine_type,
    get_timing,
    create_medicine,
    create_timing,
    delete_medicine,
    create_medicine_type,
    get_unique_medicine,
    medicine_to_type,
)

urlpatterns = [
    path("<int:id>/", MedicineAPI.as_view()),
    path("get/", get_medicine, name="get_medicine"),
    path("get/<int:id>", get_medicine, name="get_medicine"),
    path("get_or/", get_or_medicine, name="get_or_medicine"),
    path("get_or/<int:id>", get_or_medicine, name="get_or_medicine"),
    path("create/", create_medicine),
    path("delete/", delete_medicine),
    path("update-medicine/<int:id>/", patch_medicine),

    path("unique_medicine/",get_unique_medicine,name="unique_medicine"),
    path("get_medicine_type/", medicine_to_type, name="medicine_to_type"),


    
    path("type/<int:id>/", MedicineTypeAPI.as_view()),
    path("type/get/", get_medicine_type),
    path("type/get/<int:id>", get_medicine_type),
    path("type/create/", create_medicine_type),
    path("type/delete/", delete_medicine_type),
    path("update-type/<int:id>/", patch_medicine_type),
    
    path("timing/<int:id>/", TimingAPI.as_view()),
    path("timing/get/", get_timing),
    path("timing/get/<int:id>", get_timing),
    path("timing/create/", create_timing),
    path("timing/delete/", delete_timing),
    path("update-timing/<int:id>/", patch_timing),
]
