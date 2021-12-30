from django.urls import path

from .views import CityAPI, patch

urlpatterns = [
    path('<int:id>/', CityAPI.as_view()),
    path('get/', CityAPI.as_view()),
    path('create/', CityAPI.as_view()),
    path('delete/', CityAPI.as_view()),
    path('update/<int:id>/', patch, name="update"),
]
