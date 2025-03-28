from rest_framework import serializers
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

    def create(self, validated_data):
        if not validated_data.get('created_at'):
            validated_data['created_at'] = timezone.now()
        return super().create(validated_data)


class ClassModuleAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassModuleAssignment
        fields = '__all__'

    def create(self, validated_data):
        if not validated_data.get('assigned_date'):
            validated_data['assigned_date'] = timezone.now()
        if not validated_data.get('due_date'):
            validated_data['due_date'] = datetime.date.today()
        return super().create(validated_data)


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class ClassCourseMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassCourseMapping
        fields = '__all__'

    def create(self, validated_data):
        if not validated_data.get('assigned_date'):
            validated_data['assigned_date'] = timezone.now()
        return super().create(validated_data)


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

    def create(self, validated_data):
        if not validated_data.get('created_at'):
            validated_data['created_at'] = timezone.now()
        if not validated_data.get('last_modified'):
            validated_data['last_modified'] = timezone.now()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Always update last_modified to the current time on update.
        validated_data['last_modified'] = timezone.now()
        return super().update(instance, validated_data)


class UserSerializer(serializers.ModelSerializer):
    password_hash = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        if not validated_data.get('created_at'):
            validated_data['created_at'] = timezone.now()
        return super().create(validated_data)


class UserBadgeAchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBadgeAchievement
        fields = '__all__'

    def create(self, validated_data):
        if not validated_data.get('earned_date'):
            validated_data['earned_date'] = timezone.now()
        return super().create(validated_data)


class UserClassRosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserClassRoster
        fields = '__all__'

    def create(self, validated_data):
        if not validated_data.get('enrollment_date'):
            validated_data['enrollment_date'] = datetime.date.today()
        return super().create(validated_data)


class UserCourseEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCourseEnrollment
        fields = '__all__'


class UserModuleProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModuleProgress
        fields = '__all__'

    def create(self, validated_data):
        if not validated_data.get('completion_date'):
            validated_data['completion_date'] = timezone.now()
        return super().create(validated_data)


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
