from django.core.exceptions import PermissionDenied
from functools import wraps

def validate_permission(app_name, method_type):
    def method_wrapper(func):
        @wraps(func)
        def check_permission(request,id=None):
            permission = app_name + "."+ method_type.lower() + "_" + app_name.replace("_","") + "model"
            if not request.user.has_perm(permission):
                pass
                # raise PermissionDenied
            return func(request,id)
        return check_permission
    return method_wrapper