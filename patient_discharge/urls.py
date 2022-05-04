from django.urls import path

from .views import PatientDischargeAPI, patch, get, create, delete

urlpatterns = [
    path('<int:id>/', PatientDischargeAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', create),
    path('delete/', delete),
    path('update/<int:id>/', patch),
]
