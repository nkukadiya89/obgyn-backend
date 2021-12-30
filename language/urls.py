from django.urls import path

from .views import LanguageAPI, patch

urlpatterns = [
    path('<int:id>/', LanguageAPI.as_view()),
    path('get/', LanguageAPI.as_view()),
    path('create/', LanguageAPI.as_view()),
    path('delete/', LanguageAPI.as_view()),
    path('update/<int:id>/', patch),
]
