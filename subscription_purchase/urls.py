from django.urls import path

from .views import (Subscription_purchaseAPI,patch,get,
create,
delete,
)

urlpatterns = [
    path("<int:id>/", Subscription_purchaseAPI.as_view()),
    path("get/", get),
    path("get/<int:id>", get),
    path("create/", create),
    path("delete/", delete),
    path("update/<int:id>/", patch),

]