from doctest import FAIL_FAST
import six
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from functools import wraps
from django.urls import reverse
from django.contrib.auth.models import Permission

#==================================== manage field decorators=============================

def get_decorator_mf(func):
    @wraps(func)
    def check_permission(request):
        # print(Permission.objects.filter(user=request.user.id).first().__dict__)
        if not request.user.has_perm("manage_fields.view_managefieldsmodel"):
            raise PermissionDenied
        return func(request)

    return check_permission

def post_decorator_mf(func):
    @wraps(func)
    def check_permission(request):
        if not request.user.has_perm("manage_fields.add_managefieldsmodel"):
            raise PermissionDenied
        return func(request)
    return check_permission

def update_decorator_mf(func):
    @wraps(func)
    def check_permission(request):
        if not request.user.has_perm("manage_fields.change_managefieldsmodel"):
            raise PermissionDenied
        return func(request)
    return check_permission


def delete_decorator_mf(func):
    @wraps(func)
    def check_permission(request):
        if not request.user.has_perm("manage_fields.delete_managefieldsmodel"):
            raise PermissionDenied
        return func(request)
    return check_permission


#====================================manage field master decorators=============================
def get_decorator_mfm(func):
    @wraps(func)
    def check_permission(request):
        # print(Permission.objects.filter(user=request.user.id).first().__dict__)
        if not request.user.has_perm("manage_fields.view_fieldmastermodel"):
            raise PermissionDenied
        return func(request)

    return check_permission

def post_decorator_mfm(func):
    @wraps(func)
    def check_permission(request):
        if not request.user.has_perm("manage_fields.add_fieldmastermodel"):
            raise PermissionDenied
        return func(request)
    return check_permission

def update_decorator_mfm(func):
    @wraps(func)
    def check_permission(request):
        if not request.user.has_perm("manage_fields.change_fieldmastermodel"):
            raise PermissionDenied
        return func(request)
    return check_permission


def delete_decorator_mf(func):
    @wraps(func)
    def check_permission(request):
        if not request.user.has_perm("manage_fields.delete_fieldmastermodel"):
            raise PermissionDenied
        return func(request)
    return check_permission
