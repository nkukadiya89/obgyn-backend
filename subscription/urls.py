from django.urls import path, include

from .views import SubscriptionAPI, get, create, delete

urlpatterns = [
    path('<int:id>/', SubscriptionAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', create),
    path('delete/',delete),
    path('subscription_purchase/', include('subscription_purchase.urls')),
]