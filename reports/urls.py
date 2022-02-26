from django.urls import path
from .views import view_report

urlpatterns = [
    path('report-name/<int:id>', view_report, name="view_report"),
]