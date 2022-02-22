from django.urls import path

from .views import PatientBillingAPI, patch, get

urlpatterns = [
    path('<int:id>/', PatientBillingAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', PatientBillingAPI.as_view()),
    path('delete/', PatientBillingAPI.as_view()),
    path('update/<int:id>/', patch),

]
