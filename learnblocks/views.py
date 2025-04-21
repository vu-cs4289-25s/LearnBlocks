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

from rest_framework import generics, views, authentication, status

from .permissions import permissions
from .enums import RosterRole, UserRole, CourseVisibility, ModuleVisibility

from rest_framework.response import Response

from django.db.models import Q
from django.shortcuts import get_object_or_404


# --- Authentication ---
class WhoAmIView(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)

class LogoutView(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # delete the token to force a logout
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# --- Badges ---
class BadgeListCreateView(generics.ListCreateAPIView):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated
                          & (permissions.IsAdmin
                              | permissions.IsReadOnly)]


class BadgeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    lookup_field = 'badge_id'
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsReadOnly | permissions.IsAdmin]


# --- Classes ---
class ClassListCreateView(generics.ListCreateAPIView):
    serializer_class = ClassSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated
                          & (permissions.IsAdmin
                             | permissions.IsTeacher
                             | (permissions.IsStudent
                                 & permissions.IsReadOnly))]

    def get_queryset(self):
        if self.request.user.role == UserRole.ADMIN:
            return Class.objects.all()
        else:
            return Class.objects.filter(member=self.request.user)

    def perform_create(self, serializer):
        class_obj = serializer.save()
        UserClassRoster.objects.create(user=self.request.user,
                                       class_field=class_obj,
                                       role=RosterRole.OWNER)


class ClassDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClassSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated
                          & (permissions.IsAdmin
                             | permissions.IsClassOwner
                             | (permissions.IsClassMember
                                 & permissions.IsReadOnly))]
    lookup_field = 'class_id'

    def get_queryset(self):
        if self.request.user.role == UserRole.ADMIN:
            return Class.objects.all()
        else:
            return Class.objects.filter(member=self.request.user)


class ClassJoinView(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, join_code):
        class_obj = get_object_or_404(Class.objects, join_code=join_code)
        UserClassRoster.objects.create(member=self.request.user,
                                       class_field=class_obj,
                                       role=RosterRole.PARTICIPANT)
        return Response({'detail': 'Successfully joined'},
                        status=status.HTTP_201_CREATED)


# --- ClassCourseMapping---
class ClassCourseListCreateView(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated
                          & (permissions.IsAdmin
                             | permissions.IsClassOwner
                              | (permissions.IsClassMember
                                  & permissions.IsReadOnly))]
    serializer_class = ClassCourseMappingSerializer

    def get_queryset(self):
        class_id = self.kwargs.get('class_id')
        return ClassCourseMapping.objects.filter(class_field=class_id)

    def perform_create(self, serializer):
        class_id = self.kwargs.get('class_id')
        class_obj = get_object_or_404(Class.objects, class_id=class_id)
        serializer.save(class_field=class_obj)


class ClassCourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClassCourseMappingSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated
                          & (permissions.IsAdmin
                             | permissions.IsClassOwner
                              | (permissions.IsClassMember
                                  & permissions.IsReadOnly))]

    def get_object(self):
        class_id = self.kwargs.get('class_id')
        course_id = self.kwargs.get('course_id')
        assignment_obj = ClassCourseMapping.objects.get(class_field=class_id,
                                                        course=course_id)
        return assignment_obj


class ClassCourseModuleListView(generics.ListAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated
                          & (permissions.IsAdmin
                             | permissions.IsClassOwner
                             | permissions.IsClassMember)]
    serializer_class = CourseModuleMappingSerializer

    def get_queryset(self):
        class_id = self.kwargs.get('class_id')
        course_id = self.kwargs.get('course_id')
        class_course = get_object_or_404(ClassCourseMapping.objects,
                                         class_field=class_id,
                                         course=course_id)
        course = class_course.course
        course_modules = CourseModuleMapping.objects.filter(course=course)
        return course_modules


class ClassCourseModuleDetailView(generics.RetrieveAPIView):
    serializer_class = CourseModuleMappingSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated
                          & (permissions.IsAdmin
                             | permissions.IsClassOwner
                              | (permissions.IsClassMember
                                  & permissions.IsReadOnly))]

    def get_object(self):
        class_id = self.kwargs.get('class_id')
        course_id = self.kwargs.get('course_id')
        module_id = self.kwargs.get('module_id')
        class_course = get_object_or_404(ClassCourseMapping.objects,
                                         class_field=class_id,
                                         course=course_id)
        course = class_course.course
        course_module = get_object_or_404(CourseModuleMapping.objects,
                                          course=course,
                                          module=module_id)
        return course_module


class ClassCourseModuleSubmissionListView(generics.ListAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated
                          & (permissions.IsAdmin
                             | permissions.IsClassOwner
                              | permissions.IsClassMember)]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        class_id = self.kwargs.get('class_id')
        course_id = self.kwargs.get('course_id')
        module_id = self.kwargs.get('module_id')

        members = UserClassRoster.objects.filter(class_field=class_id
                                                 ).values_list('user',
                                                               flat=True)
        class_course = get_object_or_404(ClassCourseMapping.objects,
                                         class_field=class_id,
                                         course=course_id)
        course = class_course.course
        course_module = get_object_or_404(CourseModuleMapping.objects,
                                          course=course,
                                          module=module_id)
        module = course_module.module
        submissions = Project.objects.filter(owner__in=members,
                                             module=module)
        is_owner = members.filter(role=RosterRole.OWNER,
                                  user=self.request.user
                                  ).exists()
        if not is_owner:
            submissions = submissions.objects.filter(owner=self.request.user)
        return submissions


class ClassCourseModuleSubmissionDetailView(generics.RetrieveAPIView):
    serializer_class = ProjectSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated
                          & (permissions.IsAdmin
                             | permissions.IsClassOwner
                              | (permissions.IsClassMember
                                  & permissions.IsReadOnly))]

    def get_object(self):
        class_id = self.kwargs.get('class_id')
        course_id = self.kwargs.get('course_id')
        module_id = self.kwargs.get('module_id')
        project_id = self.kwargs.get('project_id')

        members = UserClassRoster.objects.filter(class_field=class_id
                                                 ).values_list('user',
                                                               flat=True)
        class_course = get_object_or_404(ClassCourseMapping.objects,
                                         class_field=class_id,
                                         course=course_id)
        course = class_course.course
        course_module = get_object_or_404(CourseModuleMapping.objects,
                                          course=course,
                                          module=module_id)
        module = course_module.module
        submissions = Project.objects.filter(owner__in=members,
                                             module=module)
        is_owner = members.filter(role=RosterRole.OWNER,
                                  user=self.request.user
                                  ).exists()
        if not is_owner:
            submissions = submissions.objects.filter(owner=self.request.user)

        project = get_object_or_404(submissions,
                                    module=module,
                                    project_id=project_id)
        return project


# --- ClassModuleAssignment ---
class ClassModuleListCreateView(generics.ListCreateAPIView):
    serializer_class = ClassModuleAssignmentSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated
                          & (permissions.IsAdmin
                             | permissions.IsClassOwner
                             | (permissions.IsClassMember
                                 & permissions.IsReadOnly))]

    def get_queryset(self):
        class_id = self.kwargs.get('class_id')
        return ClassModuleAssignment.objects.filter(class_field=class_id)

    def perform_create(self, serializer):
        class_id = self.kwargs.get('class_id')
        class_obj = get_object_or_404(Class.objects, class_id=class_id)
        serializer.save(class_field=class_obj)


class ClassModuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated
                          & (permissions.IsAdmin
                             | permissions.IsClassOwner
                             | (permissions.IsClassMember
                                 & permissions.IsReadOnly))]
    serializer_class = ClassModuleAssignmentSerializer

    def get_object(self):
        class_id = self.kwargs.get('class_id')
        module_id = self.kwargs.get('module_id')
        assignment_obj = get_object_or_404(ClassModuleAssignment.objects,
                                           module=module_id,
                                           class_field=class_id)
        return assignment_obj


class ClassModuleSubmissionListView(generics.ListAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated
                          & (permissions.IsAdmin
                             | permissions.IsClassOwner
                              | permissions.IsClassMember)]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        class_id = self.kwargs.get('class_id')
        module_id = self.kwargs.get('module_id')

        members = UserClassRoster.objects.filter(class_field=class_id
                                                 ).values_list('user',
                                                               flat=True)
        class_module = get_object_or_404(ClassModuleAssignment.objects,
                                         class_field=class_id,
                                         module=module_id)
        module = class_module.module
        submissions = Project.objects.filter(owner__in=members,
                                             module=module)
        is_owner = members.filter(role=RosterRole.OWNER,
                                  user=self.request.user
                                  ).exists()
        if not is_owner:
            submissions = submissions.objects.filter(owner=self.request.user)
        return submissions


class ClassModuleSubmissionDetailView(generics.RetrieveAPIView):
    serializer_class = ProjectSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated
                          & (permissions.IsAdmin
                             | permissions.IsClassOwner
                              | (permissions.IsClassMember
                                  & permissions.IsReadOnly))]

    def get_object(self):
        class_id = self.kwargs.get('class_id')
        module_id = self.kwargs.get('module_id')
        project_id = self.kwargs.get('project_id')

        members = UserClassRoster.objects.filter(class_field=class_id
                                                 ).values_list('user',
                                                               flat=True)

        class_module = get_object_or_404(ClassModuleAssignment.objects,
                                         class_field=class_id,
                                         module=module_id)
        module = class_module.module
        submissions = Project.objects.filter(owner__in=members,
                                             module=module)

        is_owner = members.filter(role=RosterRole.OWNER,
                                  user=self.request.user
                                  ).exists()
        print(submissions)
        if not is_owner:
            submissions = submissions.objects.filter(owner=self.request.user)

        project = get_object_or_404(submissions,
                                    project_id=project_id)
        return project


class ClassMemberListView(generics.ListAPIView):
    serializer_class = UserClassRosterSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated
                          & (permissions.IsAdmin
                             | permissions.IsClassOwner
                             | permissions.IsClassMember)]

    def get_queryset(self):
        class_id = self.kwargs.get('class_id')
        return UserClassRoster.objects.filter(class_field=class_id)


class ClassMemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserClassRosterSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated
                          & (permissions.IsAdmin
                             | permissions.IsClassOwner
                             | (permissions.IsClassMember
                                 & permissions.IsReadOnly))]

    def get_object(self):
        class_id = self.kwargs.get('class_id')
        username = self.kwargs.get('username')
        roster_entry = get_object_or_404(UserClassRoster.objects,
                                         class_field=class_id,
                                         user=username)
        return roster_entry


# --- Course ---
class CourseListCreateView(generics.ListCreateAPIView):
    serializer_class = CourseSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated
                          & (permissions.IsAdmin
                             | permissions.IsReadOnly)]

    def get_queryset(self):
        user = self.request.user
        public = CourseVisibility.PUBLIC
        if (user.role == UserRole.ADMIN):
            return Course.objects.all()
        else:
            return Course.objects.filter(Q(owner=user) | Q(visibility=public))

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated
                          & (permissions.IsAdmin
                              | permissions.IsReadOnly)]
    lookup_field = 'course_id'

    def get_queryset(self):
        user = self.request.user
        public = CourseVisibility.PUBLIC
        if (user.role == UserRole.ADMIN):
            return Course.objects.all()
        else:
            return Course.objects.filter(Q(owner=user) | Q(visibility=public))


class CourseEnrollView(generics.CreateAPIView):
    serializer_class = UserCourseEnrollment
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        course_id = self.kwargs.get('course_id')
        course = Course.objects.get(course_id=course_id)
        serializer.save(course=course,
                        user=self.request.user)


# --- CourseModuleMapping ---
class CourseModuleListCreateView(generics.ListCreateAPIView):
    serializer_class = CourseModuleMappingSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated
                          & (permissions.IsAdmin
                             | permissions.IsCourseOwner
                             | permissions.IsReadOnly)]

    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        return CourseModuleMapping.objects.filter(course=course_id)

    def perform_create(self, serializer):
        course_id = self.kwargs.get('course_id')
        course = Course.objects.get(course_id=course_id)
        serializer.save(course=course)


class CourseModuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseModuleMappingSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated
                          & (permissions.IsAdmin
                             | permissions.IsCourseOwner
                             | permissions.IsReadOnly)]

    def get_object(self):
        course_id = self.kwargs.get('course_id')
        module_id = self.kwargs.get('module_id')
        entry_obj = get_object_or_404(CourseModuleMapping.objects,
                                      course=course_id,
                                      module=module_id)
        return entry_obj


class CourseModuleSubmissionListView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        module_id = self.kwargs.get('module_id')

        course_module = get_object_or_404(CourseModuleMapping.objects,
                                          course=course_id,
                                          module=module_id)
        module = course_module.module
        is_admin = self.request.user.role == UserRole.ADMIN
        submissions = Project.objects.filter(module=module)
        if not is_admin:
            submissions = submissions.filter(owner=self.request.user)
        return submissions


class CourseModuleSubmissionDetailView(generics.RetrieveAPIView):
    serializer_class = ProjectSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        course_id = self.kwargs.get('course_id')
        module_id = self.kwargs.get('module_id')
        project_id = self.kwargs.get('project_id')

        course_module = get_object_or_404(CourseModuleMapping.objects,
                                          course=course_id,
                                          module=module_id)
        module = course_module.module
        is_admin = self.request.user.role == UserRole.ADMIN
        submissions = Project.objects.filter(module=module)
        if not is_admin:
            submissions = submissions.filter(owner=self.request.user)
        project = get_object_or_404(submissions,
                                    module=module,
                                    project_id=project_id)
        return project


# --- Module ---
class ModuleListCreateView(generics.ListCreateAPIView):
    serializer_class = ModuleSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated
                          & (permissions.IsAdmin
                             | permissions.IsReadOnly)]

    def get_queryset(self):
        user = self.request.user
        public = ModuleVisibility.PUBLIC
        if (user.role == UserRole.ADMIN):
            return Module.objects.all()
        else:
            return Module.objects.filter(Q(owner=user) | Q(visibility=public))

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ModuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ModuleSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated
                          & (permissions.IsAdmin
                             | permissions.IsReadOnly)]
    lookup_field = 'module_id'

    def get_queryset(self):
        user = self.request.user
        public = ModuleVisibility.PUBLIC
        if (user.role == UserRole.ADMIN):
            return Module.objects.all()
        else:
            return Module.objects.filter(Q(owner=user) | Q(visibility=public))


class UserModuleListCreateView(generics.ListCreateAPIView):
    serializer_class = UserModuleProgress
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'module_id'

    def get_queryset(self):
        user = self.request.user
        modules = UserModuleProgress.objects.filter(user=user)
        return modules


class ModuleSubmissionListCreateView(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        module_id = self.kwargs.get('module_id')

        is_admin = self.request.user.role == UserRole.ADMIN
        submissions = Project.objects.filter(module=module_id)
        if not is_admin:
            submissions = submissions.filter(owner=self.request.user)
        return submissions

    def perform_create(self, serializer):
        user = self.request.user
        module_id = self.kwargs.get('module_id')
        module = get_object_or_404(Module.objects, module_id=module_id)
        serializer.save(module=module, owner=user)


class ModuleSubmissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        module_id = self.kwargs.get('module_id')
        project_id = self.kwargs.get('project_id')

        is_admin = self.request.user.role == UserRole.ADMIN
        submissions = Project.objects.all()
        if not is_admin:
            submissions = submissions.filter(owner=self.request.user)
        project = get_object_or_404(submissions,
                                    module=module_id,
                                    project_id=project_id)
        return project

    def perform_destroy(self, instance: Project):
        instance.module = None
        instance.save()


# --- Project ---
class ProjectListCreateView(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        user = self.request.user
        if (user.role != UserRole.ADMIN):
            return Project.objects.all()
        return Project.objects.filter(owner=user)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user)
        pass


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated
                          & (permissions.IsAdmin
                             | permissions.IsProjectOwner)]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    lookup_field = 'project_id'


# --- User ---
class UserListCreateView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [~permissions.IsReadOnly
                          | permissions.IsAuthenticated]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated
                          & (permissions.IsAdmin
                             | permissions.IsSelf)]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


# --- UserBadgeAchievement ---
class UserBadgeListView(generics.ListAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserBadgeAchievement.objects.all()
    serializer_class = UserBadgeAchievementSerializer


class UserBadgeDetailView(generics.RetrieveAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserBadgeAchievement.objects.all()
    serializer_class = UserBadgeAchievementSerializer
    lookup_field = 'achievement_id'
