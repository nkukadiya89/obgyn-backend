from django.urls import path

from city import views
from .views import CityAPI

urlpatterns = [
    path('<int:id>/', CityAPI.as_view()),
    path('get/', CityAPI.as_view()),
    path('create/', CityAPI.as_view()),
    path('delete/', CityAPI.as_view()),
    path('update/<int:id>/', views.patch, name="update"),
]
