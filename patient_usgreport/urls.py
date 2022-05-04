from django.urls import path

from advice.views import delete

from .views import PatientUSGReportAPI, patch, get, create, delete

urlpatterns = [
    path('<int:id>/', PatientUSGReportAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', create),
    path('delete/', delete),
    path('update/<int:id>/', patch),

]
