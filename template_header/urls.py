from django.urls import path

from .views import TemplateHeaderAPI, patch, get

urlpatterns = [
    path('<int:id>/', TemplateHeaderAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', TemplateHeaderAPI.as_view()),
    path('delete/', TemplateHeaderAPI.as_view()),
    path('update/<int:id>/', patch, name="update"),
]
