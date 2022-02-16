from django.urls import path

from .views import PatientMtpAPI, patch, get

urlpatterns = [
    path('<int:id>/', PatientMtpAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', PatientMtpAPI.as_view()),
    path('delete/', PatientMtpAPI.as_view()),
    path('update/<int:id>/', patch),

]
