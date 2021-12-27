from django.urls import path

from .views import ManageFieldsAPI

urlpatterns = [
    path('<int:id>/', ManageFieldsAPI.as_view()),
    path('get/', ManageFieldsAPI.as_view()),
    path('create/', ManageFieldsAPI.as_view()),
    path('delete/', ManageFieldsAPI.as_view()),
]
