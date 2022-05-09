from django.urls import path

from .views import (
    SurgicalItemAPI,
    SurgicalItemGroupAPI,
    patch,
    patch_surgical_group,
    get,
    get_group,
    create,
    create_group,
    delete,
    delete_group,
)

urlpatterns = [
    path("<int:id>/", SurgicalItemAPI.as_view()),
    path("get/", get),
    path("get/<int:id>", get),
    path("create/", create),
    path("delete/", delete),
    path("update-item/<int:id>/", patch),
    
    path("group/<int:id>/", SurgicalItemGroupAPI.as_view()),
    path("group/get/", get_group),
    path("group/get/<int:id>", get_group),
    path("group/create/", create_group),
    path("group/delete/", delete_group),
    path("update-group/<int:id>/", patch_surgical_group),
]
