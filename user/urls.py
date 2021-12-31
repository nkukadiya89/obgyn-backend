from django.urls import path

from user.views import register_view, get_user, change_password, forget_password, reset_password, update_user, \
    delete_user, verify_user, send_verify_link

urlpatterns = [
    path('create/', register_view, name="register_user"),
    path('update/<int:id>/', update_user, name="update_user"),
    path('get/<str:type>/', get_user),
    path('get/<str:type>/<int:id>/', get_user),
    path('change_password/', change_password, name="change_password"),
    path('forget_password/', forget_password, name="forget_password"),
    path('reset_password/<str:token>', reset_password, name="reset_password"),
    path('send_verify_token/', send_verify_link, name="send_verify_link"),
    path('verify_token/<str:token>', verify_user, name="verify_user"),
    path('delete/', delete_user, name="delete_user")
]
