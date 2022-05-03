from django.core.exceptions import PermissionDenied
from functools import wraps

def decorator(app_name, method_type):
    def method_wrapper(func):
        @wraps(func)
        def check_permission(request):
            permission = app_name + "."+ method_type.lower() + "_" + app_name.replace("_","") + "model"
            if not request.user.has_perm(permission):
                raise PermissionDenied
            return func(request)
        return check_permission
    return method_wrapper