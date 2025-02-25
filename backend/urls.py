"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from learnblocks import views

router = routers.DefaultRouter()
router.register(r'learnblocks', views.LearnBlocksView, 'learnblocks')

router.register(r'user',views.UserViewSet,basename='user')
router.register(r'badge',views.BadgeViewSet,basename='badge')
router.register(r'activity',views.ActivityViewSet,basename='activity')
router.register(r'class',views.ClassViewSet,basename='class')
router.register(r'course',views.CourseViewSet,basename='course')
router.register(r'module',views.ModuleViewSet,basename='module')
router.register(r'progress',views.ProgressViewSet,basename='progress')
router.register(r'assignment',views.AssignmentViewSet,basename='assignment')
router.register(r'session',views.SessionViewSet,basename='session')
router.register(r'project',views.ProjectViewSet,basename='project')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
