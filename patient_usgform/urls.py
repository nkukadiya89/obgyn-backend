from django.urls import path

from .views import PatientUSGFormAPI, patch, get,USGFormChildAPI, child_patch, child_get

urlpatterns = [
    path('<int:id>/', PatientUSGFormAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', PatientUSGFormAPI.as_view()),
    path('delete/', PatientUSGFormAPI.as_view()),
    path('update/<int:id>/', patch),

    path('child/<int:id>/', USGFormChildAPI.as_view()),
    path('child/get/', child_get),
    path('child/get/<int:id>', child_get),
    path('child/create/', USGFormChildAPI.as_view()),
    path('child/delete/', USGFormChildAPI.as_view()),
    path('child/update/<int:id>/', child_patch),

]
