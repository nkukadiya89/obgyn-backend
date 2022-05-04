from django.urls import path

from .views import PatientIndoorAPI, patch, get, create, delete,  IndoorAdviceAPI, indoor_advice_patch, indoor_advice_get

urlpatterns = [
    path('<int:id>/', PatientIndoorAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', delete),
    path('delete/', create),
    path('update/<int:id>/', patch),

    path('advice/<int:id>/', IndoorAdviceAPI.as_view()),
    path('advice/get/', indoor_advice_get),
    path('advice/get/<int:id>', indoor_advice_get),
    path('advice/create/', create),
    path('advice/delete/', delete),
    path('advice/update/<int:id>/', indoor_advice_patch),

]
