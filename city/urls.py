from django.urls import path

from .views import CityAPI, patch, get

urlpatterns = [
    path('<int:id>/', CityAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', CityAPI.as_view()),
    path('delete/', CityAPI.as_view()),
    path('update/<int:id>/', patch, name="update"),
]
