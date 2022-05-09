from django.urls import path

from city.views import delete

from .views import (
    PatientIndoorAPI,
    patch,
    get,
    IndoorAdviceAPI,
    indoor_advice_patch,
    indoor_advice_get,
    create,
    create_advice,
    delete,
    delete_advice,
)

urlpatterns = [
    path("<int:id>/", PatientIndoorAPI.as_view()),
    path("get/", get),
    path("get/<int:id>", get),
    path("create/", create),
    path("delete/", delete),
    path("update/<int:id>/", patch),
    
    path("advice/<int:id>/", IndoorAdviceAPI.as_view()),
    path("advice/get/", indoor_advice_get),
    path("advice/get/<int:id>", indoor_advice_get),
    path("advice/create/", create_advice),
    path("advice/delete/", delete_advice),
    path("advice/update/<int:id>/", indoor_advice_patch),
]
