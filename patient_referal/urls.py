from django.urls import path

from advice.views import delete

from .views import PatientReferalAPI, patch, get, delete, create

urlpatterns = [
    path('<int:id>/', PatientReferalAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', create),
    path('delete/', delete),
    path('update/<int:id>/', patch),
]
