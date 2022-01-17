from django.urls import path

from .views import ManageFieldsAPI, patch, get, FieldMasterAPI, field_patch,field_get

urlpatterns = [
    path('<int:id>/', ManageFieldsAPI.as_view()),
    path('get/', get),
    path('get/<int:id>', get),
    path('create/', ManageFieldsAPI.as_view()),
    path('delete/', ManageFieldsAPI.as_view()),
    path('update/<int:id>/', patch),

    path('field/<int:id>/', FieldMasterAPI.as_view()),
    path('field/get/', field_get),
    path('field/get/<int:id>', field_get),
    path('field/create/', FieldMasterAPI.as_view()),
    path('field/delete/', FieldMasterAPI.as_view()),
    path('field/update/<int:id>/', field_patch),

]
