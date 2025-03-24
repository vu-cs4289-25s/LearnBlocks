from rest_framework import serializers
#from .models import LearnBlocks
from .models import *

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
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class CourseClassMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseClassMapping
        fields = '__all__'

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'

class ModuleCourseMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleCourseMapping
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    password_hash = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = '__all__'

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
        #model = LearnBlocks
        model=Badge
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