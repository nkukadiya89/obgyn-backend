from django.urls import path

from user.views import register_view

urlpatterns = [
    path('create/', register_view),

]
