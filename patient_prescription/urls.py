from django.urls import path

from .views import PatientPrescriptionAPI, patch, get

urlpatterns = [
    path('<int:id>/', PatientPrescriptionAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', PatientPrescriptionAPI.as_view()),
    path('delete/', PatientPrescriptionAPI.as_view()),
    path('update/<int:id>/', patch),
]
