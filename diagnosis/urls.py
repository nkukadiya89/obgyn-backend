from django.urls import path

from .views import DiagnosisAPI, patch, get

urlpatterns = [
    path('<int:id>/', DiagnosisAPI.as_view()),
    path('get/', get),
    path('get/<int:int>', get),
    path('create/', DiagnosisAPI.as_view()),
    path('delete/', DiagnosisAPI.as_view()),
    path('update/<int:id>/', patch),
]
