from django.urls import path

from .views import StateAPI

urlpatterns = [
    path('get', StateAPI.as_view()),
    path('create/', StateAPI.as_view()),
    path('<int:id>', StateAPI.as_view()),
]
