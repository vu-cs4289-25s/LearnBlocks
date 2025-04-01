from rest_framework.permissions import BasePermission, IsAuthenticated
from ..enums import enums


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == enums.UserRole.ADMIN)


class IsTeacherOrAdminUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and
                    (request.user.role == enums.UserRole.TEACHER or
                        request.user.role == enums.UserRole.ADMIN))


__all__ = ["IsTeacherOrAdminUser", "IsAdminUser", "IsAuthenticated"]
