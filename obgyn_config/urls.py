from django.urls import path
from .views import (ObgynConfigAPI,patch,get,create,)

urlpatterns = [
    path("<int:id>/", ObgynConfigAPI.as_view()),
    path("get/", get),
    path("get/<int:id>", get),
    path("create/", create),
    path("update/<int:id>/", patch),
]