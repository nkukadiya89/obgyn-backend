from django.urls import path, include

from .views import ConsultationAPI, patch, get, create, delete

urlpatterns = [
    path('<int:id>/', ConsultationAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', create),
    path('delete/', delete),
    path('update/<int:id>/', patch, name="update"),
    path('prescription/',include('patient_prescription.urls')),
]
