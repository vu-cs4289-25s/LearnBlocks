from rest_framework import serializers
from .models import LearnBlocks

class LearnBlocksSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearnBlocks
        fields = ('id', 'title', 'description', 'completed')