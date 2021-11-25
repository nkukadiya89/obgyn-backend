from django.urls import path

from .views import CityAPI

urlpatterns = [
    path('get', CityAPI.as_view()),
    path('create/', CityAPI.as_view()),
    path('<int:id>', CityAPI.as_view()),
]
