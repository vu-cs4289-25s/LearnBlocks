from rest_framework import serializers
from ..models import (UserClassRoster, ClassCourseMapping,
                      ClassModuleAssignment, CourseModuleMapping,
                      UserBadgeAchievement, Project, UserCourseEnrollment,
                      UserModuleProgress)


def is_included(serializer, field):
    include = field in getattr(serializer, '_includes', {})
    return include


class UserBadgesUtilSerializer(serializers.ModelSerializer):
    image = serializers.UUIDField(source='badge.image')
    badge_id = serializers.UUIDField(source='badge.badge_id')
    badge_name = serializers.UUIDField(source='badge.badge_name')
    badge_description = serializers.CharField(source='badge.badge_description')

    class Meta:
        model = UserBadgeAchievement
        fields = ['badge_id', 'badge_name', 'badge_description', 'module_name',
                  'earned_date']


class BadgeEarnersUtilSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = UserBadgeAchievement
        fields = ['username', 'earned_date']


class UserClassEnrollmentsUtilSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='class_field.class_name')
    class_id = serializers.UUIDField(source='class_field.class_id')

    class Meta:
        model = UserClassRoster
        fields = ['class_name', 'class_id', 'role', 'enrollment_date']


class UserCourseEnrollmentsUtilSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.course_name')
    course_id = serializers.UUIDField(source='course.course_id')

    class Meta:
        model = UserCourseEnrollment
        fields = ['course_id', 'course_name']


class UserModuleProgressUtilSerializer(serializers.ModelSerializer):
    module_name = serializers.CharField(source='module.module_name')
    module_id = serializers.UUIDField(source='module.module_id')

    class Meta:
        model = UserModuleProgress
        fields = ['module_id', 'module_name', 'status', 'completion_date']


class UserProjectsUtilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['project_id', 'project_name', 'file', 'module']


class ClassMembersUtilSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = UserClassRoster
        fields = ['username', 'role', 'enrollment_date']


class ClassCoursesUtilSerializer(serializers.ModelSerializer):
    course_id = serializers.CharField(source='course.course_id')
    course_name = serializers.UUIDField(source='course.course_name')

    class Meta:
        model = ClassCourseMapping
        fields = ['course_id', 'course_name', 'assigned_date', 'due_date']


class ClassModulesUtilSerializer(serializers.ModelSerializer):
    module_id = serializers.CharField(source='module.module_id')
    module_name = serializers.UUIDField(source='module.module_name')

    class Meta:
        model = ClassModuleAssignment
        fields = ['module_id', 'module_name', 'assigned_date', 'due_date']


class CourseModulesUtilSerializer(serializers.ModelSerializer):
    module_id = serializers.CharField(source='module.module_id')
    module_name = serializers.UUIDField(source='module.module_name')

    class Meta:
        model = CourseModuleMapping
        fields = ['module_id', 'module_name', 'module_order']


class CourseMembersUtilSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = UserCourseEnrollment
        fields = ['username']


class ModuleProgressorsUtilSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = UserModuleProgress
        fields = ['username', 'status']
