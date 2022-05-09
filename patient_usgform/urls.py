from django.urls import path

from .views import PatientUSGFormAPI, patch, get,USGFormChildAPI, child_patch, child_get, create, create_child, delete, delete_child

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
    path('child/create/', create_child),
    path('child/delete/', delete_child),
    path('child/update/<int:id>/', child_patch),

]
