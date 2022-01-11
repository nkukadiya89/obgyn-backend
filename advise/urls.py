from django.urls import path

from .views import AdviseAPI, patch, get

urlpatterns = [
    path('<int:id>/', AdviseAPI.as_view()),
    path('get/', get),
    path('get/<int:int>', get),
    path('create/', AdviseAPI.as_view()),
    path('delete/', AdviseAPI.as_view()),
    path('update/<int:id>/', patch, name="update"),
]
