from django.urls import path, include

from .views import PatientAPI, patch, get

urlpatterns = [
    path('<int:id>/', PatientAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', PatientAPI.as_view()),
    path('delete/', PatientAPI.as_view()),
    path('update/<int:id>/', patch),
    path('consultation/', include('consultation.urls')),
    path('referal/', include('patient_referal.urls')),
    path('delivery/', include('patient_delivery.urls')),
    path('usgform/', include('patient_usgform.urls')),
    path('discharge/', include('patient_discharge.urls')),
    path('usgreport/',include('patient_usgreport.urls')),
    path('ovulation-profile/', include('patient_ovulation_profile.urls')),
]
