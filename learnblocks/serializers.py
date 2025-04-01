from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
import datetime
from .models import (Badge, Class, ClassModuleAssignment, Course,
                     ClassCourseMapping, Module, CourseModuleMapping,
                     Project, User, UserBadgeAchievement, UserClassRoster,
                     UserCourseEnrollment, UserModuleProgress)


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = '__all__'


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'


class ClassModuleAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassModuleAssignment
        fields = ['module', 'due_date']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class ClassCourseMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassCourseMapping
        fields = '__all__'


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'


class CourseModuleMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseModuleMapping
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True,
                                     validators=[validate_password])

    class Meta:
        model = User
        fields = ['username', 'email', 'password',
                  'first_name', 'last_name', 'role']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')

        if request and request.user != instance:
            data.pop('email', None)

        return data


class UserBadgeAchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBadgeAchievement
        fields = '__all__'


class UserClassRosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserClassRoster
        fields = '__all__'


class UserCourseEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCourseEnrollment
        fields = '__all__'


class UserModuleProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModuleProgress
        fields = '__all__'


class LearnBlocksSerializer(serializers.ModelSerializer):
    class Meta:
        # model = LearnBlocks
        model = Badge
        fields = ('id', 'title', 'description', 'completed')


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
