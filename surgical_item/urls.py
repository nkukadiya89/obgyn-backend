from django.urls import path

from .views import SurgicalItemAPI,SurgicalItemGroupAPI, patch, patch_surgical_group, get, get_group

urlpatterns = [
    path('<int:id>/', SurgicalItemAPI.as_view()),
    path('get/', get),
    path('create/', SurgicalItemAPI.as_view()),
    path('delete/', SurgicalItemAPI.as_view()),
    path('update-item/<int:id>/', patch),

    path('group/<int:id>/', SurgicalItemGroupAPI.as_view()),
    path('group/get/', get_group),
    path('group/create/', SurgicalItemGroupAPI.as_view()),
    path('group/delete/', SurgicalItemGroupAPI.as_view()),
    path('update-group/<int:id>/', patch_surgical_group),

]
