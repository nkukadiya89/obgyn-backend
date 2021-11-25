from django.urls import path

from .views import LanguageAPI

urlpatterns = [
    path('get', LanguageAPI.as_view()),
    path('create/', LanguageAPI.as_view()),
    path('<int:id>', LanguageAPI.as_view()),
]
