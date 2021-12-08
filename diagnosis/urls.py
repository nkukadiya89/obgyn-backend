from django.urls import path

from .views import DiagnosisAPI

urlpatterns = [
    path('<int:id>/', DiagnosisAPI.as_view()),
    path('get/', DiagnosisAPI.as_view()),
    path('create/', DiagnosisAPI.as_view()),
    path('delete/<int:id>/', DiagnosisAPI.as_view()),
]
