from django.urls import path

from .views import DiagnosisAPI, patch

urlpatterns = [
    path('<int:id>/', DiagnosisAPI.as_view()),
    path('get/', DiagnosisAPI.as_view()),
    path('create/', DiagnosisAPI.as_view()),
    path('delete/', DiagnosisAPI.as_view()),
    path('update/<int:id>/', patch),
]
