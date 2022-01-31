from django.urls import path

from .views import PatientDischargeAPI, patch, get

urlpatterns = [
    path('<int:id>/', PatientDischargeAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', PatientDischargeAPI.as_view()),
    path('delete/', PatientDischargeAPI.as_view()),
    path('update/<int:id>/', patch),
]
