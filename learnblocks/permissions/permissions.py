from rest_framework.permissions import (BasePermission, IsAuthenticated,
                                        SAFE_METHODS, AllowAny)
from ..enums import UserRole, RosterRole
from ..models import UserClassRoster, Course, Project


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.role == UserRole.ADMIN)


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.role == UserRole.TEACHER)


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.role == UserRole.STUDENT)


class IsClassOwner(BasePermission):
    def has_permission(self, request, view):
        class_id = view.kwargs.get('class_id')
        member = UserClassRoster.objects.get(user=request.user,
                                             class_field=class_id)
        is_owner = (member and member.role == RosterRole.OWNER)
        is_participant = (member and member.role ==
                          RosterRole.PARTICIPANT)
        is_get = request.method in SAFE_METHODS
        return bool((is_get and is_participant) or (is_owner))


class IsClassMember(BasePermission):
    def has_permission(self, request, view):
        class_id = view.kwargs.get('class_id')
        is_member = bool(class_id
                         and
                         UserClassRoster.objects.filter(user=request.user,
                                                        class_field=class_id,
                                                        role=RosterRole.PARTICIPANT
                                                        ).exists())
        return is_member


class IsReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS)


class IsCourseOwner(BasePermission):
    def has_permission(self, request, view):
        course_id = view.kwargs.get('course_id')
        is_owner = bool(course_id
                        and
                        Course.objects.filter(owner=request.user,
                                              course_id=course_id,
                                              ).exists())
        return bool(is_owner)


class IsSelf(BasePermission):
    def has_permission(self, request, view):
        username = view.kwargs.get('username')
        is_self = username == request.user.username
        return bool(is_self)


class IsProjectOwner(BasePermission):
    def has_permission(self, request, view):
        project_id = view.kwargs.get('project_id')
        is_owner = bool(project_id
                        and
                        Project.objects.filter(owner=request.user,
                                               project_id=project_id,
                                               ).exists())
        return is_owner
