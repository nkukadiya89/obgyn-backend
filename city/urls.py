from django.urls import path

from .views import CityAPI, patch, get, create, delete

urlpatterns = [
    path('<int:id>/', CityAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/',create),
    path('delete/', delete),
    path('update/<int:id>/', patch, name="update"),
]
