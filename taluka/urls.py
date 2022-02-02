from django.urls import path

from .views import TalukaAPI, patch, get

urlpatterns = [
    path('<int:id>/', TalukaAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', TalukaAPI.as_view()),
    path('delete/', TalukaAPI.as_view()),
    path('update/<int:id>/', patch, name="update"),
]
