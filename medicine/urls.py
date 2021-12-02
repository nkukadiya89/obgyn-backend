from django.urls import path

from .views import MedicineAPI, MedicineTypeAPI, TimingAPI

urlpatterns = [
    path('<int:id>/', MedicineAPI.as_view()),
    path('get/', MedicineAPI.as_view()),
    path('create/', MedicineAPI.as_view()),
    path('delete/<int:id>/', MedicineAPI.as_view()),

    path('type/<int:id>/', MedicineTypeAPI.as_view()),
    path('type/get/', MedicineTypeAPI.as_view()),
    path('type/create/', MedicineTypeAPI.as_view()),
    path('type/delete/<int:id>/', MedicineTypeAPI.as_view()),

    path('timing/<int:id>/', TimingAPI.as_view()),
    path('timing/get/', TimingAPI.as_view()),
    path('timing/create/', TimingAPI.as_view()),
    path('timing/delete/<int:id>/', TimingAPI.as_view()),

]
