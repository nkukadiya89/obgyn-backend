from django.urls import path

from .views import LanguageAPI

urlpatterns = [
    path('<int:id>/', LanguageAPI.as_view()),
    path('get/', LanguageAPI.as_view()),
    path('create/', LanguageAPI.as_view()),
    path('delete/<int:id>/', LanguageAPI.as_view()),
]
