from django.urls import path

from .views import StateAPI, patch, get

urlpatterns = [
    path('<int:id>/', StateAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', StateAPI.as_view()),
    path('delete/', StateAPI.as_view()),
    path('update/<int:id>/', patch),
]
