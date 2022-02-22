from django.urls import path

from .views import PatientIndoorAPI, patch, get, IndoorAdviceAPI, indoor_advice_patch, indoor_advice_get

urlpatterns = [
    path('<int:id>/', PatientIndoorAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', PatientIndoorAPI.as_view()),
    path('delete/', PatientIndoorAPI.as_view()),
    path('update/<int:id>/', patch),

    path('advice/<int:id>/', IndoorAdviceAPI.as_view()),
    path('advice/get/', indoor_advice_get),
    path('advice/get/<int:id>', indoor_advice_get),
    path('advice/create/', IndoorAdviceAPI.as_view()),
    path('advice/delete/', IndoorAdviceAPI.as_view()),
    path('advice/update/<int:id>/', indoor_advice_patch),

]
