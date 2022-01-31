from django.urls import path

from .views import PatientUSGReportAPI, patch, get

urlpatterns = [
    path('<int:id>/', PatientUSGReportAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', PatientUSGReportAPI.as_view()),
    path('delete/', PatientUSGReportAPI.as_view()),
    path('update/<int:id>/', patch),

]
