from rest_framework.permissions import BasePermission
from apps.permission.verify import verify_permission


class RBACPermission(BasePermission):
    """自定义权限"""

    @classmethod
    def get_permission_from_role(self, request):
        try:
            perms = request.user.roles.values(
                'permissions__method',
            ).distinct()
            return [p['permissions__method'] for p in perms]
        except AttributeError:
            return None

    def has_permission(self, request, view):
        perms = self.get_permission_from_role(request)
        if perms:
            if 'admin' in perms:
                return True
            elif not hasattr(view, 'perms_map'):
                return True
            else:
                perms_map = view.perms_map
                _method = request._request.method.lower()
                for i in perms_map:
                    for method, alias in i.items():
                        if (_method == method or method == '*') and alias in perms:
                            return True


class ObjPermission(BasePermission):
    """密码管理对象级权限控制"""

    def has_object_permission(self, request, view, obj):
        perms = RBACPermission.get_permission_from_role(request)
        if 'admin' in perms:
            return True
        elif request.user.id == obj.uid_id:
            return True


class ApiRBACPermission(BasePermission):
    def has_permission(self, request, view):
        path = request.META["PATH_INFO"]
        username = request.user.username
        method = request.method
        return verify_permission(username, path, method)