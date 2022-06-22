from django.core.exceptions import PermissionDenied
from functools import wraps

def validate_permission(app_name, method_type):
    def method_wrapper(func):
        # @wraps(func)
        def check_permission(request):
            request.data["created_by"] = request.user.id
            permission = app_name + "."+ method_type.lower() + "_" + app_name.replace("_","") + "model"
            if not request.user.has_perm(permission):
                pass
                # raise PermissionDenied
            return func(request)
        return check_permission
    return method_wrapper


def validate_permission_id(app_name, method_type):
    def method_wrapper(func):
        # @wraps(func)
        def check_permission(request,id=None):
            request.data["created_by"] = request.user.id
            permission = app_name + "."+ method_type.lower() + "_" + app_name.replace("_","") + "model"
            if not request.user.has_perm(permission):
                pass
                # raise PermissionDenied
            return func(request,id)
        return check_permission
    return method_wrapper