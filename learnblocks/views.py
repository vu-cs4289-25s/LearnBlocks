from django.shortcuts import render
from rest_framework import viewsets
from .serializers import LearnBlocksSerializer
from .models import LearnBlocks

# Create your views here.
class LearnBlocksView(viewsets.ModelViewSet):
    serializer_class = LearnBlocksSerializer
    queryset = LearnBlocks.objects.all()