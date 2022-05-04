from django.urls import path

from .views import LanguageAPI, patch, get, delete, create

urlpatterns = [
    path('<int:id>/', LanguageAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', create),
    path('delete/', delete),
    path('update/<int:id>/', patch),
]
