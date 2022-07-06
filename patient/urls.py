from django.urls import path, include

from .views import PatientAPI, patch, get, create, delete, get_unique_patient

urlpatterns = [
    path('<int:id>/', PatientAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', create),
    path('delete/', delete),
    path("unique_patient/", get_unique_patient, name="unique_patient"),

    path('update/<int:id>/', patch),
    path('consultation/', include('consultation.urls')),
    path('referal/', include('patient_referal.urls')),
    path('delivery/', include('patient_delivery.urls')),
    path('usgform/', include('patient_usgform.urls')),
    path('discharge/', include('patient_discharge.urls')),
    path('usgreport/', include('patient_usgreport.urls')),
    path('ovulation-profile/', include('patient_ovulation_profile.urls')),
    path('mtp/', include('patient_mtp.urls')),
    path('histolap/', include('patient_histolap.urls')),
    path('billing/', include('patient_billing.urls')),
    path('voucher/', include('patient_voucher.urls')),
    path('indoor/', include('patient_indoor.urls')),
]
