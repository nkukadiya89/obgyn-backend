from django.urls import path

from .views import PatientUSGFormAPI, patch, get, create, delete, USGFormChildAPI, child_patch, child_get

urlpatterns = [
    path('<int:id>/', PatientUSGFormAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', create),
    path('delete/', delete),
    path('update/<int:id>/', patch),

    path('child/<int:id>/', USGFormChildAPI.as_view()),
    path('child/get/', child_get),
    path('child/get/<int:id>', child_get),
    path('child/create/', create),
    path('child/delete/', delete),
    path('child/update/<int:id>/', child_patch),

]
