from django.urls import path

from .views import PatientOpdAPI, patch, get, create, delete

urlpatterns = [
    path("<int:id>/", PatientOpdAPI.as_view()),
    path("get/", get),
    path("get/<int:id>", get),
    path("create/", create),
    path("delete/", delete),
    path("update/<int:id>/", patch),
]
