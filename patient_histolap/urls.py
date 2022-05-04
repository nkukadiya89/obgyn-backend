from django.urls import path

from .views import PatientHistolapAPI, patch, get, create, delete

urlpatterns = [
    path('<int:id>/', PatientHistolapAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', create),
    path('delete/', delete),
    path('update/<int:id>/', patch),

]
