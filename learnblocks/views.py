from django.shortcuts import render
from rest_framework import viewsets
from .serializers import LearnBlocksSerializer,DynamicFieldsSerializer
from .models import LearnBlocks

from rest_framework.response import Response
from rest_framework.decorators import api_view,action

from rest_framework import serializers
from .mock import *
# Create your views here.
class LearnBlocksView(viewsets.ModelViewSet):
    serializer_class = LearnBlocksSerializer
    queryset = LearnBlocks.objects.all()


class UserViewSet(viewsets.ModelViewSet):
    """Handles user creation, retrieval, and updates"""
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  # Require login
    """
    serializer_class=LearnBlocksSerializer

    def retrieve(self, request, pk=None):
        """GET: Fetch user details by user_id"""
        """
        try:
            user = User.objects.get(pk=pk)
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        """
        return Response(mock_user)
    

    def create(self, request):
        """POST: Create a new user"""
        """
        data = request.data.copy()
        data["password"] = make_password(data["password"])  # Hash password before saving
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user_id": user.id,
                "username": user.username,
                "email": user.email
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        """
        return Response(mock_user)

    def update(self, request, pk=None):
        """PUT: Update user details"""
        """
        try:
            user = User.objects.get(pk=pk)
            data = request.data.copy()
            
            # Hash the password if it's being updated
            if "password" in data and data["password"]:
                data["password"] = make_password(data["password"])

            serializer = self.get_serializer(user, data=data, partial=True)
            if serializer.is_valid():
                user = serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        """
        return Response(mock_user)
    
    @action(detail=True, methods=['get'], url_path='badge')
    def badge(self, request, pk=None):
        """
        GET /user/:user_id/badge/
        Returns the list of badges associated with the user.
        """
        """
        user = self.get_object()  # Gets the User object with id=pk
        badges = Badge.objects.filter(student=user)
        serializer = BadgeSerializer(badges, many=True)
        return Response({"badges": serializer.data})
        """
        return Response(mock_badge_list)
    
    @action(detail=True, methods=['get'], url_path='activity')
    def activity(self, request, pk=None):  
        return Response(mock_activity_list)
    
    @action(detail=True, methods=['get'], url_path='class')
    def get_class(self, request, pk=None):  
        return Response(mock_class_list)
    @action(detail=True, methods=['post'], url_path='add_class')
    def add_class(self, request, pk=None):
        return Response(mock_rooster)
    @action(detail=True, methods=['get'], url_path='progress')
    def progress(self, request, pk=None):
        return Response(progress_list)
    
class BadgeViewSet(viewsets.ModelViewSet):
    serializer_class=LearnBlocksSerializer
    def retrieve(self, request, pk=None):
        return Response(mock_badge)
    def create(self, request, *args, **kwargs):
        return Response(mock_badge)

class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class=LearnBlocksSerializer
    def create(self, request, *args, **kwargs):
        return Response(mock_activity)

class ClassViewSet(viewsets.ModelViewSet):
    serializer_class=DynamicFieldsSerializer
    def get_queryset(self):
        return mock_class_list["classes"]
    def retrieve(self, request, *args, **kwargs):
        return Response(mock_class)
    def create(self, request, *args, **kwargs):
        return Response(mock_class)
    def update(self, request, *args, **kwargs):
        return Response(mock_class)
    def destroy(self, request, *args, **kwargs):
        return Response()
    @action(detail=True, methods=['get'], url_path='assignment')
    def assignment(self, request, pk=None):
        return Response(assignment_list)

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class=DynamicFieldsSerializer
    def get_queryset(self):
        return mock_course_list["courses"]
    def retrieve(self, request, *args, **kwargs):
        return Response(mock_course)
    def create(self, request, *args, **kwargs):
        return Response(mock_course)
    def update(self, request, *args, **kwargs):
        return Response(mock_course)
    def destroy(self, request, *args, **kwargs):
        return Response()
    @action(detail=True, methods=['get'], url_path='module')
    def module(self, request, pk=None):
        return Response(module_list)
    @action(detail=True, methods=['get'], url_path='assignment')
    def assignment(self, request, pk=None):
        return Response(assignment_list)

class ModuleViewSet(viewsets.ModelViewSet):
    serializer_class=DynamicFieldsSerializer
    def get_queryset(self):
        return modules
    def retrieve(self, request, *args, **kwargs):
        return Response(module_data_1)
    def create(self, request, *args, **kwargs):
        return Response(module_data_1)
    def update(self, request, *args, **kwargs):
        return Response(module_data_1)
    def destroy(self, request, *args, **kwargs):
        return Response()    
    @action(detail=True, methods=['get'], url_path='progress')
    def progress(self, request, pk=None):
        return Response(progress_list)

    
class ProgressViewSet(viewsets.ModelViewSet):
    serializer_class=DynamicFieldsSerializer
    def get_queryset(self):
        return progresses
    def retrieve(self, request, *args, **kwargs):
        return Response(progress_data_1)
    def create(self, request, *args, **kwargs):
        return Response(progress_data_1)
    def update(self, request, *args, **kwargs):
        return Response(progress_data_1)
    def destroy(self, request, *args, **kwargs):
        return Response() 

class AssignmentViewSet(viewsets.ModelViewSet):
    serializer_class=DynamicFieldsSerializer
    def get_queryset(self):
        return assignments
    def retrieve(self, request, *args, **kwargs):
        return Response(assignment_data_1)
    def create(self, request, *args, **kwargs):
        return Response(assignment_data_1)
    def update(self, request, *args, **kwargs):
        return Response(assignment_data_1)
    def destroy(self, request, *args, **kwargs):
        return Response()     
    
class SessionViewSet(viewsets.ModelViewSet):
    serializer_class=DynamicFieldsSerializer
    def create(self, request, *args, **kwargs):
        request.session['user'] = mock_session
        return Response(mock_session)
    @action(detail=False, methods=['delete'], url_path='reset')
    def reset_session(self, request, *args, **kwargs):
        request.session.flush()
        return Response()
    