from django.urls import path

from user.permission_management import create_new_group, assign_user_group, list_permission, assign_permission_group, \
    get_group_permission, list_group
from user.views import register_view, get_user, change_password, forget_password, reset_password, update_user, \
    delete_user, verify_user, send_verify_link

urlpatterns = [
    path('create/', register_view, name="register_user"),
    path('update/<int:id>/', update_user, name="update_user"),
    path('get/<str:type>/', get_user),
    path('get/<str:type>/<int:id>/', get_user),
    path('change-password/', change_password, name="change_password"),
    path('forget-password/', forget_password, name="forget_password"),
    path('reset-password/<str:token>', reset_password, name="reset_password"),
    path('verify-email/', send_verify_link, name="send_verify_link"),
    path('verify-token/<str:token>', verify_user, name="verify_user"),
    path('delete/', delete_user, name="delete_user"),

    path('create-group/', create_new_group, name="create_new_group"),
    path('get-group/',list_group,name="get_group"),
    path('get-group/<int:id>',list_group,name="get_group"),
    path('assign-user-group/', assign_user_group, name="assign_user_group"),
    path('list-permission/', list_permission, name="list_permission"),
    path('assign-permission-group/', assign_permission_group, name="assign_permission_group"),
    path('get-group-permisison/<int:user_id>', get_group_permission, name="get_group_permission")
]
