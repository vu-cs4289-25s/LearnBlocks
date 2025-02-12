from rest_framework import serializers
from .models import LearnBlocks

class LearnBlocksSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearnBlocks
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