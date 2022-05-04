from django.urls import path

from .views import DistrictAPI, patch, get, delete, create

urlpatterns = [
    path('<int:id>/', DistrictAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', create),
    path('delete/', delete),
    path('update/<int:id>/', patch, name="update"),
]
