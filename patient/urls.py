from django.urls import path

from .views import PatientAPI, patch, get

urlpatterns = [
    path('<int:id>/', PatientAPI.as_view()),
    path('get/', get),
    path('create/', PatientAPI.as_view()),
    path('delete/', PatientAPI.as_view()),
    path('update/<int:id>/', patch),
]
