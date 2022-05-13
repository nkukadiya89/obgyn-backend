from django.urls import path

from .views import TemplateHeaderAPI, patch, get, create, delete

urlpatterns = [
    path('<int:id>/', TemplateHeaderAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', create),
    path('delete/', delete),
    path('update/<int:id>/', patch, name="update"),
]
