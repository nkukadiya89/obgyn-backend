from django.urls import path

from .views import *

urlpatterns = [
    path('<int:id>/', ManageFieldsAPI.as_view()),
    path('get/', get_mf),
    path('get/<int:id>', get_mf),
    path('create/', create_mf),
    path('delete/', delete_mf),
    path('update/<int:id>/', patch_mf),

    path('field/<int:id>/', FieldMasterAPI.as_view()),
    path('field/get/', get_mfm),
    path('field/get/<int:id>', get_mfm),
    path('field/create/', create_mfm),
    path('field/delete/', delete_mfm),
    path('field/update/<int:id>/', patch_mfm),

]
