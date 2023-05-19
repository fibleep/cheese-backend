#authx/permissions.py
from rest_framework.permissions import BasePermission

class IsUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role >=0 )
class IsManagerUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role >= 2)
class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role >= 3 or request.user.is_superuser)
     