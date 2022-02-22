from django.urls import path

from .views import PatientHistolapAPI, patch, get

urlpatterns = [
    path('<int:id>/', PatientHistolapAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', PatientHistolapAPI.as_view()),
    path('delete/', PatientHistolapAPI.as_view()),
    path('update/<int:id>/', patch),

]
