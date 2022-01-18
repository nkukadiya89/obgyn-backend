from django.urls import path

from .views import AdviceAPI, patch, get, AdviceGroupAPI, patch_group, get_group

urlpatterns = [
    path('<int:id>/', AdviceAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', AdviceAPI.as_view()),
    path('delete/', AdviceAPI.as_view()),
    path('update/<int:id>/', patch, name="update"),

    path('group/<int:id>/', AdviceGroupAPI.as_view()),
    path('group/get/', get_group),
    path('group/get/<int:id>', get_group),
    path('group/create/', AdviceGroupAPI.as_view()),
    path('group/delete/', AdviceGroupAPI.as_view()),
    path('group/update/<int:id>/', patch_group, name="update"),

]
