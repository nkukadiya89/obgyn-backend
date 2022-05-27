from django.urls import path
from .views import (Obgyn_ConfigAPI,patch_obgyn_config,get_obgyn_config,create_obgyn_config,)

urlpatterns = [
    path("<int:id>/", Obgyn_ConfigAPI.as_view()),
    path("get/", get_obgyn_config),
    path("get/<int:id>", get_obgyn_config),
    path("create/", create_obgyn_config),
    path("update/<int:id>/", patch_obgyn_config),
]