from django.urls import path

from .views import PatientPrescriptionAPI, patch, get, create, delete

urlpatterns = [
    path('<int:id>/', PatientPrescriptionAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', create),
    path('delete/', delete),
    path('update/<int:id>/', patch),
]
