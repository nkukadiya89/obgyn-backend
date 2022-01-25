from django.urls import path

from .views import PatientOpdAPI, patch, get

urlpatterns = [
    path('<int:id>/', PatientOpdAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', PatientOpdAPI.as_view()),
    path('delete/', PatientOpdAPI.as_view()),
    path('update/<int:id>/', patch),
]
