from django.urls import path

from .views import LanguageAPI, patch, get

urlpatterns = [
    path('<int:id>/', LanguageAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', LanguageAPI.as_view()),
    path('delete/', LanguageAPI.as_view()),
    path('update/<int:id>/', patch),
]
