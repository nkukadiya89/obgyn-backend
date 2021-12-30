from django.urls import path

from .views import StateAPI, patch

urlpatterns = [
    path('<int:id>/', StateAPI.as_view()),
    path('get/', StateAPI.as_view()),
    path('create/', StateAPI.as_view()),
    path('delete/', StateAPI.as_view()),
    path('update/<int:id>/', patch),
]
