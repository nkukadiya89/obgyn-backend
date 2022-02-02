from django.urls import path

from .views import DistrictAPI, patch, get

urlpatterns = [
    path('<int:id>/', DistrictAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', DistrictAPI.as_view()),
    path('delete/', DistrictAPI.as_view()),
    path('update/<int:id>/', patch, name="update"),
]
