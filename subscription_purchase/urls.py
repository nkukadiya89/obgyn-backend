from django.urls import path
from .views import (Subscription_purchaseAPI,patch_subscription_purchase,get_subscription_purchase,
create_subscription_purchase,
delete_Subscription_purchase,
)

urlpatterns = [
    path("<int:id>/", Subscription_purchaseAPI.as_view()),
    path("get/", get_subscription_purchase),
    path("get/<int:id>", get_subscription_purchase),
    path("create/", create_subscription_purchase),
    path("delete/", delete_Subscription_purchase),
    path("update/<int:id>/", patch_subscription_purchase),
]