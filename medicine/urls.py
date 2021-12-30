from django.urls import path

from .views import MedicineAPI, MedicineTypeAPI, TimingAPI, patch_medicine, patch_timing, patch_medicine_type

urlpatterns = [
    path('<int:id>/', MedicineAPI.as_view()),
    path('get/', MedicineAPI.as_view()),
    path('create/', MedicineAPI.as_view()),
    path('delete/', MedicineAPI.as_view()),
    path('update_medicine/<int:id>/', patch_medicine),

    path('type/<int:id>/', MedicineTypeAPI.as_view()),
    path('type/get/', MedicineTypeAPI.as_view()),
    path('type/create/', MedicineTypeAPI.as_view()),
    path('type/delete/<int:id>/', MedicineTypeAPI.as_view()),
    path('update_type/<int:id>/', patch_medicine_type),

    path('timing/<int:id>/', TimingAPI.as_view()),
    path('timing/get/', TimingAPI.as_view()),
    path('timing/create/', TimingAPI.as_view()),
    path('timing/delete/<int:id>/', TimingAPI.as_view()),
    path('update_timing/<int:id>/', patch_timing),
]
