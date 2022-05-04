from django.urls import path

from .views import MedicineAPI, MedicineTypeAPI, TimingAPI, patch_medicine, patch_timing, patch_medicine_type, \
    get_medicine, get_or_medicine, get_medicine_type, create, delete

urlpatterns = [
    path('<int:id>/', MedicineAPI.as_view()),
    path('get/', get_medicine, name="get_medicine"),
    path('get/<int:id>', get_medicine, name="get_medicine"),

    path('get_or/', get_or_medicine, name="get_or_medicine"),
    path('get_or/<int:id>', get_or_medicine, name="get_or_medicine"),

    path('create/', create),
    path('delete/', delete),
    path('update-medicine/<int:id>/', patch_medicine),

    path('type/<int:id>/', MedicineTypeAPI.as_view()),
    path('type/get/', get_medicine_type),
    path('type/get/<int:id>', get_medicine_type),
    path('type/create/', create),
    path('type/delete/', delete),
    path('update-type/<int:id>/', patch_medicine_type),

    path('timing/<int:id>/', TimingAPI.as_view()),
    path('timing/get/', TimingAPI.as_view()),
    path('timing/get/<int:id>', TimingAPI.as_view()),
    path('timing/create/', create),
    path('timing/delete/', delete),
    path('update-timing/<int:id>/', patch_timing),
]
