from django.urls import path

from .views import ManageFieldsAPI, patch, get

urlpatterns = [
    path('<int:id>/', ManageFieldsAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', ManageFieldsAPI.as_view()),
    path('delete/', ManageFieldsAPI.as_view()),
    path('update/<int:id>/', patch),
]
