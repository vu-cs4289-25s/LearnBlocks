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

from rest_framework import generics, views, authentication, permissions 
from rest_framework.response import Response


# --- Authentication ---
class WhoAmIView(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class BadgeListView(generics.ListCreateAPIView):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer


class BadgeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    lookup_field = 'badge_id'


class ClassListCreateView(generics.ListCreateAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class ClassRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    lookup_field = 'class_id'


# --- ClassModuleAssignment ---
class ClassModuleAssignmentListCreateView(generics.ListCreateAPIView):

    queryset = ClassModuleAssignment.objects.all()
    serializer_class = ClassModuleAssignmentSerializer


class ClassModuleAssignmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClassModuleAssignment.objects.all()
    serializer_class = ClassModuleAssignmentSerializer
    lookup_field = 'assignment_id'


# --- Course ---
class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'course_id'


# --- CourseClassMapping ---
# Note: This model uses a composite key; we use the 'course' field as lookup.
class ClassCourseMappingListCreateView(generics.ListCreateAPIView):
    queryset = ClassCourseMapping.objects.all()
    serializer_class = ClassCourseMappingSerializer


class ClassCourseMappingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClassCourseMapping.objects.all()
    serializer_class = ClassCourseMappingSerializer
    lookup_field = 'course'


# --- Module ---
class ModuleListCreateView(generics.ListCreateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer


class ModuleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    lookup_field = 'module_id'


# --- ModuleCourseMapping ---
# Note: Composite key; we use the 'course' field as lookup.
class CourseModuleMappingListCreateView(generics.ListCreateAPIView):
    queryset = CourseModuleMapping.objects.all()
    serializer_class = CourseModuleMappingSerializer


class CourseModuleMappingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CourseModuleMapping.objects.all()
    serializer_class = CourseModuleMappingSerializer
    lookup_field = 'course'


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
# Note: Uses 'user' as primary key (composite key workaround)
class UserClassRosterListCreateView(generics.ListCreateAPIView):
    queryset = UserClassRoster.objects.all()
    serializer_class = UserClassRosterSerializer


class UserClassRosterRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserClassRoster.objects.all()
    serializer_class = UserClassRosterSerializer
    lookup_field = 'user'


# --- UserCourseEnrollment ---
# Note: Uses 'user' as primary key (composite key workaround)
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
