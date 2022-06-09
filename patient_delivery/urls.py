from django.urls import path

from .views import PatientDeliveryAPI, patch, get, create, delete, get_sequence

urlpatterns = [
    path('<int:id>/', PatientDeliveryAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/',create),
    path('delete/', delete),
    path('update/<int:id>/', patch),
    path('get_seq/',get_sequence),
]
