from django.urls import path

from .views import SurgicalItemAPI,SurgicalItemGroupAPI, patch, patch_surgical_group

urlpatterns = [
    path('<int:id>/', SurgicalItemAPI.as_view()),
    path('get/', SurgicalItemAPI.as_view()),
    path('create/', SurgicalItemAPI.as_view()),
    path('delete/', SurgicalItemAPI.as_view()),
    path('update_item/<int:id>/', patch),

    path('group/<int:id>/', SurgicalItemGroupAPI.as_view()),
    path('group/get/', SurgicalItemGroupAPI.as_view()),
    path('group/create/', SurgicalItemGroupAPI.as_view()),
    path('group/delete/<int:id>/', SurgicalItemGroupAPI.as_view()),
    path('update_group/<int:id>/', patch_surgical_group),

]
