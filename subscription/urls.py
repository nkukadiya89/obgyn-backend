from django.urls import path

from .views import SubscriptionAPI, get

urlpatterns = [
    path('<int:id>/', SubscriptionAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', SubscriptionAPI.as_view()),
    path('delete/', SubscriptionAPI.as_view()),
 
]