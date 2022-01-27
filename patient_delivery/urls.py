from django.urls import path

from .views import PatientDeliveryAPI, patch, get

urlpatterns = [
    path('<int:id>/', PatientDeliveryAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', PatientDeliveryAPI.as_view()),
    path('delete/', PatientDeliveryAPI.as_view()),
    path('update/<int:id>/', patch),
]
