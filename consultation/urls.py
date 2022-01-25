from django.urls import path, include

from .views import ConsultationAPI, patch, get

urlpatterns = [
    path('<int:id>/', ConsultationAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', ConsultationAPI.as_view()),
    path('delete/', ConsultationAPI.as_view()),
    path('update/<int:id>/', patch, name="update"),
    path('prescription/',include('patient_prescription.urls')),
]