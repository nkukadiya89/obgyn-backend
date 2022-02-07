from django.urls import path

from .views import PatientOvulationProfileAPI, patch, get

urlpatterns = [
    path('<int:id>/', PatientOvulationProfileAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', PatientOvulationProfileAPI.as_view()),
    path('delete/', PatientOvulationProfileAPI.as_view()),
    path('update/<int:id>/', patch),

]
