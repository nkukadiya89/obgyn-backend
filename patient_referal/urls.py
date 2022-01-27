from django.urls import path

from .views import PatientReferalAPI, patch, get

urlpatterns = [
    path('<int:id>/', PatientReferalAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', PatientReferalAPI.as_view()),
    path('delete/', PatientReferalAPI.as_view()),
    path('update/<int:id>/', patch),
]
