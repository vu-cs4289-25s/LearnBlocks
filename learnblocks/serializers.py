from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import (Badge, Class, ClassModuleAssignment, Course,
                     ClassCourseMapping, Module, CourseModuleMapping,
                     Project, User, UserBadgeAchievement, UserClassRoster,
                     UserCourseEnrollment, UserModuleProgress)
from .enums import UserRole
from .utils.serializers import is_included

from .utils.serializers import (BadgeEarnersUtilSerializer,
                                UserClassEnrollmentsUtilSerializer,
                                UserBadgesUtilSerializer,
                                UserProjectsUtilSerializer,
                                UserCourseEnrollmentsUtilSerializer,
                                UserModuleProgressUtilSerializer,
                                ClassMembersUtilSerializer,
                                ClassCoursesUtilSerializer,
                                ClassModulesUtilSerializer,
                                CourseModulesUtilSerializer,
                                CourseMembersUtilSerializer,
                                ModuleProgressorsUtilSerializer)


class BadgeSerializer(serializers.ModelSerializer):
    recipients = serializers.SerializerMethodField()

    def get_recipients(self, obj: Badge):
        recipients = UserBadgeAchievement.objects.filter(badge=obj)
        return BadgeEarnersUtilSerializer(recipients, many=True).data

    class Meta:
        model = Badge
        fields = '__all__'


class ClassSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()
    courses = serializers.SerializerMethodField()
    modules = serializers.SerializerMethodField()

    def get_members(self, obj: Class):
        if is_included(serializer=self):
            return
        roster_entries = UserClassRoster.objects.filter(class_field=obj)
        return ClassMembersUtilSerializer(roster_entries, many=True).data

    def get_courses(self, obj: Class):
        class_courses = ClassCourseMapping.objects.filter(class_field=obj)
        return ClassCoursesUtilSerializer(class_courses, many=True).data

    def get_modules(self, obj: Class):
        class_modules = ClassModuleAssignment.objects.filter(class_field=obj)
        return ClassModulesUtilSerializer(class_modules, many=True).data

    class Meta:
        model = Class
        fields = ['class_id', 'class_name', 'members', 'courses', 'modules',
                  'is_active', 'created_at']


class ClassModuleAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassModuleAssignment
        fields = ['module', 'due_date']

    def update(self, instance, validated_data):
        if 'module' in validated_data:
            raise serializers.ValidationError(
                {"module": "This field cannot be updated."})
        return super().update(instance, validated_data)


class CourseSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    modules = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()

    def get_modules(self, obj: Course):
        course_modules = CourseModuleMapping.objects.filter(course=obj)
        return CourseModulesUtilSerializer(course_modules, many=True).data

    def get_members(self, obj: Course):
        users = UserCourseEnrollment.objects.filter(course=obj)
        return CourseMembersUtilSerializer(users, many=True).data

    class Meta:
        model = Course
        fields = ['course_id', 'course_name', 'owner', 'badge',
                  'modules', 'members', 'status', 'visibility']


class ClassCourseMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassCourseMapping
        fields = '__all__'
        extra_kwargs = {'class_field': {'read_only': True}}

    def update(self, instance, validated_data):
        if 'course' in validated_data:
            raise serializers.ValidationError(
                {"course": "This field cannot be updated."})
        return super().update(instance, validated_data)


class ModuleSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    progressors = serializers.SerializerMethodField()

    def get_progressors(self, obj: Module):
        users = UserModuleProgress.objects.filter(module=obj)
        return ModuleProgressorsUtilSerializer(users, many=True).data

    class Meta:
        model = Module
        fields = ['module_id', 'module_name', 'owner', 'file', 'progressors']


class CourseModuleMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseModuleMapping
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['project_id', 'project_name', 'owner', 'file', 'module']
        extra_kwargs = {'owner': {'read_only': True},
                        'module': {'read_only': True}}


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True,
                                     validators=[validate_password])
    role = serializers.ChoiceField(choices=[
        (UserRole.TEACHER, "Teacher"),
        (UserRole.STUDENT, "Student"),
    ])
    class_enrollments = serializers.SerializerMethodField()
    course_enrollments = serializers.SerializerMethodField()
    module_progressions = serializers.SerializerMethodField()
    badge_awards = serializers.SerializerMethodField()
    projects = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        self._includes = set()

        if request:
            includes_param = request.query_params.get('include')
            if includes_param:
                self._includes = set(i.strip()
                                     for i in includes_param.split(','))

    def get_projects(self, user):
        if not is_included(serializer=self, field='projects'):
            return None
        projects = Project.objects.filter(owner=user)
        return UserProjectsUtilSerializer(projects, many=True).data

    def get_class_enrollments(self, user):
        include = 'class_enrollments' in getattr(self, '_includes', {})
        if not include:
            return None
        roster = UserClassRoster.objects.filter(member=user)
        return UserClassEnrollmentsUtilSerializer(roster, many=True).data

    def get_course_enrollments(self, user):
        include = 'course_enrollments' in getattr(self, '_includes', {})
        if not include:
            return None
        roster = UserCourseEnrollment.objects.filter(user=user)
        return UserCourseEnrollmentsUtilSerializer(roster, many=True).data

    def get_module_progressions(self, user):
        include = 'module_progressions' in getattr(self, '_includes', {})
        if not include:
            return None
        progresses = UserModuleProgress.objects.filter(user=user)
        return UserModuleProgressUtilSerializer(progresses, many=True).data

    def get_badge_awards(self, user):
        include = 'badge_awards' in getattr(self, '_includes', {})
        if not include:
            return None
        badges = UserBadgeAchievement.objects.filter(user=user)
        return UserBadgesUtilSerializer(badges, many=True).data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        is_self = (request and request.user == instance)
        if not request or not is_self:
            data.pop('email', None)
        optional_fields = ['class_enrollments', 'course_enrollments',
                           'module_progressions', 'badge_awards', 'projects'
                           ]
        for field in optional_fields:
            if field not in getattr(self, '_includes', {}):
                data.pop(field, None)
        return data

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name',
                  'class_enrollments', 'course_enrollments',
                  'module_progressions', 'role', 'projects',  'badge_awards']


class UserBadgeAchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBadgeAchievement
        fields = '__all__'


class UserClassRosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserClassRoster
        fields = '__all__'
        extra_kwargs = {'class_field': {'read_only': True},
                        'user': {'read_only': True}}

    def update(self, instance, validated_data):
        if 'class_field' in validated_data:
            raise serializers.ValidationError(
                {"class_field": "This field cannot be updated."})
        return super().update(instance, validated_data)


class UserCourseEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCourseEnrollment
        fields = '__all__'
        extra_kwargs = {'class_field': {'read_only': True}}

    def update(self, instance, validated_data):
        if 'class_field' in validated_data:
            raise serializers.ValidationError(
                {"class_field": "This field cannot be updated."})
        return super().update(instance, validated_data)


class UserModuleProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModuleProgress
        fields = '__all__'


class DynamicFieldsSerializer(serializers.Serializer):
    """
    A serializer that accepts all input fields without validation.
    Use this only when you do not need strict validation.
    """

    def to_internal_value(self, data):
        if not isinstance(data, dict):
            self.fail('invalid')
        # Simply return the data as-is.
        return data

    def to_representation(self, instance):
        # instance is assumed to be a dict
        return instance
