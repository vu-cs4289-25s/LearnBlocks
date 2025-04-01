from .models import (Badge, Class, ClassModuleAssignment, Course,
                     ClassCourseMapping, Module, CourseModuleMapping,
                     Project, User, UserBadgeAchievement, UserClassRoster,
                     UserCourseEnrollment, UserModuleProgress)

from .serializers import (BadgeSerializer, ClassSerializer,
                          ClassModuleAssignmentSerializer, CourseSerializer,
                          ClassCourseMappingSerializer, ModuleSerializer,
                          CourseModuleMappingSerializer, ProjectSerializer,
                          UserSerializer, UserBadgeAchievementSerializer,
                          UserClassRosterSerializer,
                          UserCourseEnrollmentSerializer,
                          UserModuleProgressSerializer)

from rest_framework import generics, views, authentication, exceptions
from .permissions import permissions
from .enums import RosterRole, UserRole, CourseVisibility

from rest_framework.response import Response

from django.db.models import Q


# --- Authentication ---
class WhoAmIView(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# --- Badges ---
class BadgeListCreateView(generics.ListCreateAPIView):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]


class BadgeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    lookup_field = 'badge_id'

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]


class ClassListCreateView(generics.ListCreateAPIView):
    serializer_class = ClassSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(),
                    permissions.IsTeacherOrAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.role == UserRole.ADMIN:
            return Class.objects.all()
        else:
            return Class.objects.filter(member=self.request.user)

    def perform_create(self, serializer):
        class_obj = serializer.save()
        class_obj.members.add(self.request.user)


class ClassRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ClassSerializer
    queryset = Class.objects.all()
    lookup_field = 'class_id'

    def get_object(self):
        obj = super().get_object()

        is_owner = UserClassRoster.objects.filter(
            user=self.request.user,
            class_field=obj,
            role=RosterRole.OWNER
        ).exists()
        is_participant = UserClassRoster.objects.filter(
            user=self.request.user,
            class_field=obj,
            role=RosterRole.PARTICIPANT
        ).exists()
        is_get = self.request.method == 'GET'

        if not (is_get and is_participant) and not (is_owner):
            raise exceptions.PermissionDenied(
                "You must be an owner of this class to modify it.")
        return obj


# --- Module ---
class ModuleListCreateView(generics.ListCreateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer


class ModuleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    lookup_field = 'module_id'


# --- Course ---
class CourseListCreateView(generics.ListCreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if (user.role != UserRole.Admin):
            return Course.objects.all()
        return Course.objects.filter(Q(owner=user) or Q(visibility=CourseVisibility.PUBLIC))

    def perform_create(self, serializer):
        if (self.request.user.role != UserRole.ADMIN):
            raise exceptions.PermissionDenied(
                "You are not authorized to add a course")
        serializer.save(owner=self.request.user)


class CourseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Course.objects.all()

    def get_object(self):
        course_id = self.kwargs.get('course_id')
        assignment_obj = Course.objects.get(course_id=course_id)
        is_get = self.request.method == 'GET'
        is_admin = self.request.user.role == UserRole.ADMIN

        if not (is_get) and not (is_admin):
            raise exceptions.PermissionDenied(
                "You are not authorized to modify courses.")
        return assignment_obj


# --- ClassModuleAssignment ---
class ClassModuleAssignmentListCreateView(generics.ListCreateAPIView):
    serializer_class = ClassModuleAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        class_id = self.kwargs.get('class_id')
        if not class_id:
            raise exceptions.ParseError(
                "Missing required URL parameter: class_id")
        return ClassModuleAssignment.objects.filter(class_field=class_id)

    def perform_create(self, serializer):
        class_id = self.kwargs.get('class_id')
        class_obj = Class.objects.get(class_id=class_id)
        is_owner = UserClassRoster.objects.filter(
            user=self.request.user,
            class_field=class_obj,
            role=RosterRole.OWNER
        ).exists()
        if not is_owner:
            raise exceptions.PermissionDenied(
                "You must be an owner of this class to add a module.")
        serializer.save(class_field=class_obj)


class ClassModuleAssignmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClassModuleAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        class_id = self.kwargs.get('class_id')
        if not class_id:
            raise exceptions.ParseError(
                "Missing required URL parameter: class_id")
        return ClassModuleAssignment.objects.filter(class_field=class_id)

    def get_object(self):
        class_id = self.kwargs.get('class_id')
        module_id = self.kwargs.get('module_id')
        assignment_obj = ClassModuleAssignment.objects.get(class_field=class_id,
                                                           module=module_id)
        is_owner = UserClassRoster.objects.filter(
            user=self.request.user,
            class_field=class_id,
            role=RosterRole.OWNER
        ).exists()
        is_participant = UserClassRoster.objects.filter(
            user=self.request.user,
            class_field=class_id,
            role=RosterRole.PARTICIPANT
        ).exists()
        is_get = self.request.method == 'GET'

        if not (is_get and is_participant) and not (is_owner):
            raise exceptions.PermissionDenied(
                "You must be an owner of this class to modify its assignments.")
        return assignment_obj


# --- ClassCourseMapping---
class ClassCourseMappingListCreateView(generics.ListCreateAPIView):
    serializer_class = ClassCourseMappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        class_id = self.kwargs.get('class_id')
        if not class_id:
            raise exceptions.ParseError(
                "Missing required URL parameter: class_id")
        return ClassCourseMapping.objects.filter(class_field=class_id)

    def perform_create(self, serializer):
        class_id = self.kwargs.get('class_id')
        class_obj = Class.objects.get(class_id=class_id)
        is_owner = UserClassRoster.objects.filter(
            user=self.request.user,
            class_field=class_obj,
            role=RosterRole.OWNER
        ).exists()
        if not is_owner:
            raise exceptions.PermissionDenied(
                "You must be an owner of this class to add a course.")
        serializer.save(class_field=class_obj)


class ClassCourseMappingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClassCourseMappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        class_id = self.kwargs.get('class_id')
        if not class_id:
            raise exceptions.ParseError(
                "Missing required URL parameter: class_id")
        return ClassCourseMapping.objects.filter(class_field=class_id)

    def get_object(self):
        class_id = self.kwargs.get('class_id')
        course_id = self.kwargs.get('course_id')
        assignment_obj = ClassCourseMapping.objects.get(class_field=class_id,
                                                        course=course_id)
        is_owner = UserClassRoster.objects.filter(
            user=self.request.user,
            class_field=class_id,
            role=RosterRole.OWNER
        ).exists()
        is_participant = UserClassRoster.objects.filter(
            user=self.request.user,
            class_field=class_id,
            role=RosterRole.PARTICIPANT
        ).exists()
        is_get = self.request.method == 'GET'

        if not (is_get and is_participant) and not (is_owner):
            raise exceptions.PermissionDenied(
                "You must be an owner of this class to modify its assignments.")
        return assignment_obj


# --- CourseModuleMapping ---
class CourseModuleMappingListCreateView(generics.ListCreateAPIView):
    serializer_class = CourseModuleMappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        if not course_id:
            raise exceptions.ParseError(
                "Missing required URL parameter: course_id")
        return CourseModuleMapping.objects.filter(course=course_id)

    def perform_create(self, serializer):
        course_id = self.kwargs.get('course_id')
        is_owner = Course.objects.filter(
            course_id=course_id,
            owner=self.request.user
        ).exists()
        if not is_owner:
            raise exceptions.PermissionDenied(
                "You must be the owner to add a module to a course")
        serializer.save()


class CourseModuleMappingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseModuleMappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        if not course_id:
            raise exceptions.ParseError(
                "Missing required URL parameter: course_id")
        return CourseModuleMapping.objects.filter(course=course_id)

    def get_object(self):
        course_id = self.kwargs.get('course_id')
        module_id = self.kwargs.get('module_id')
        entry_obj = CourseModuleMapping.objects.get(course=course_id,
                                                    module=module_id)
        is_owner = Course.objects.filter(
            course_id=course_id,
            owner=self.request.user
        ).exists()
        is_get = self.request.method == 'GET'

        if not (is_get) and not (is_owner):
            raise exceptions.PermissionDenied(
                "You must be an owner of this course to modify its modules.")
        return entry_obj


# --- Project ---
class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'project_id'


# --- User ---
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'user_id'


# --- UserBadgeAchievement ---
class UserBadgeAchievementListCreateView(generics.ListCreateAPIView):
    queryset = UserBadgeAchievement.objects.all()
    serializer_class = UserBadgeAchievementSerializer


class UserBadgeAchievementRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserBadgeAchievement.objects.all()
    serializer_class = UserBadgeAchievementSerializer
    lookup_field = 'achievement_id'


# --- UserClassRoster ---
class UserClassRosterListCreateView(generics.ListCreateAPIView):
    queryset = UserClassRoster.objects.all()
    serializer_class = UserClassRosterSerializer


class UserClassRosterRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserClassRoster.objects.all()
    serializer_class = UserClassRosterSerializer
    lookup_field = 'user'


# --- UserCourseEnrollment ---
class UserCourseEnrollmentListCreateView(generics.ListCreateAPIView):
    queryset = UserCourseEnrollment.objects.all()
    serializer_class = UserCourseEnrollmentSerializer


class UserCourseEnrollmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserCourseEnrollment.objects.all()
    serializer_class = UserCourseEnrollmentSerializer
    lookup_field = 'user'


# --- UserModuleProgress ---
class UserModuleProgressListCreateView(generics.ListCreateAPIView):
    queryset = UserModuleProgress.objects.all()
    serializer_class = UserModuleProgressSerializer


class UserModuleProgressRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserModuleProgress.objects.all()
    serializer_class = UserModuleProgressSerializer
    lookup_field = 'progress_id'
