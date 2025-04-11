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
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from learnblocks import views

urlpatterns = [
    # Admin endpoint:
    path('admin/', admin.site.urls),

    # Auth endpoints:
    path('login/', obtain_auth_token),
    path('whoami/', views.WhoAmIView.as_view(), name='who-am-i'),

    # Badge endpoints:
    path('badges/',
         views.BadgeListCreateView.as_view(),
         name='badge-list'),
    path('badges/<uuid:badge_id>/',
         views.BadgeDetailView.as_view(),
         name='badge-detail'),

    # Class endpoints:
    path('classes/',
         views.ClassListCreateView.as_view(),
         name='class-list'),
    path('classes/<uuid:class_id>/',
         views.ClassDetailView.as_view(),
         name='class-detail'),

    path('classes/join/<uuid:join_code>/',
         views.ClassJoinView.as_view(),
         name='class-join'),

    path('classes/<uuid:class_id>/courses/',
         views.ClassCourseListCreateView.as_view(),
         name='class-courses-list'),
    path('classes/<uuid:class_id>/courses/<uuid:course_id>/',
         views.ClassCourseDetailView.as_view(),
         name='class-courses-detail'),

    path('classes/<uuid:class_id>/courses/<uuid:course_id>/modules/',
         views.ClassCourseModuleListView.as_view(),
         name='class-course-module-list'),
    path('classes/<uuid:class_id>/courses/<uuid:course_id>/modules/<uuid:module_id>/',
         views.ClassCourseModuleDetailView.as_view(),
         name='class-course-modules-detail'),

    path('classes/<uuid:class_id>/courses/<uuid:course_id>/modules/<uuid:module_id>/submissions/',
         views.ClassCourseModuleSubmissionListView.as_view(),
         name='class-course-module-submission-list'),
    path('classes/<uuid:class_id>/courses/<uuid:course_id>/modules/<uuid:module_id>/submissions/<uuid:project_id>/',
         views.ClassCourseModuleSubmissionDetailView.as_view(),
         name='class-course-module-submission-detail'),

    path('classes/<uuid:class_id>/modules/',
         views.ClassModuleListCreateView.as_view(),
         name='class-modules-list'),
    path('classes/<uuid:class_id>/modules/<uuid:module_id>/',
         views.ClassModuleDetailView.as_view(),
         name='class-modules-detail'),

    path('classes/<uuid:class_id>/modules/<uuid:module_id>/submissions/',
         views.ClassModuleSubmissionListView.as_view(),
         name='class-module-submissions-list'),
    path('classes/<uuid:class_id>/modules/<uuid:module_id>/submissions/<uuid:project_id>/',
         views.ClassModuleSubmissionDetailView.as_view(),
         name='class-module-submissions-detail'),
    path('classes/<uuid:class_id>/members/',
         views.ClassMemberListView.as_view(),
         name='class-users-list'),
    path('classes/<uuid:class_id>/members/<str:username>/',
         views.ClassMemberDetailView.as_view(),
         name='class-users-detail'),

    # Course endpoints:
    path('courses/',
         views.CourseListCreateView.as_view(),
         name='course-list'),
    path('courses/<uuid:course_id>/',
         views.CourseDetailView.as_view(),
         name='course-detail'),

    path('courses/<uuid:course_id>/enroll/',
         views.CourseDetailView.as_view(),
         name='course-detail'),

    path('courses/<uuid:course_id>/modules/',
         views.CourseModuleListCreateView.as_view(),
         name='course-modules-list'),
    path('courses/<uuid:course_id>/modules/<uuid:module_id>/',
         views.CourseModuleDetailView.as_view(),
         name='course-modules-detail'),

    path('courses/<uuid:course_id>/modules/<uuid:module_id>/submissions/',
         views.CourseModuleSubmissionListView.as_view(),
         name='course-module-submission-list'),
    path('courses/<uuid:course_id>/modules/<uuid:module_id>/submissions/<uuid:project_id>/',
         views.CourseModuleSubmissionDetailView.as_view(),
         name='course-module-submission-detail'),

    # Module endpoints:
    path('modules/',
         views.ModuleListCreateView.as_view(),
         name='module-list'),
    path('modules/<uuid:module_id>/',
         views.ModuleDetailView.as_view(),
         name='module-detail'),
    path('modules/<uuid:module_id>/progress',
         views.UserModuleListCreateView.as_view(),
         name='module-progress-detail'),
    path('modules/<uuid:module_id>/submissions/',
         views.ModuleSubmissionListCreateView.as_view(),
         name='module-submission-list'),
    path('modules/<uuid:module_id>/submissions/<uuid:project_id>/',
         views.ModuleSubmissionDetailView.as_view(),
         name='module-submission-detail'),

    # Project endpoints:
    path('projects/',
         views.ProjectListCreateView.as_view(),
         name='project-list'),
    path('projects/<uuid:project_id>/',
         views.ProjectDetailView.as_view(),
         name='project-detail'),

    # User endpoints:
    path('users/',
         views.UserListCreateView.as_view(),
         name='user-list'),
    path('users/<str:username>/',
         views.UserDetailView.as_view(),
         name='user-detail'),
    path('users/<str:username>/badges/',
         views.UserBadgeListView.as_view(),
         name='user-badge-list'),
    path('users/<str:username>/badges/<uuid:achievement_id>/',
         views.UserBadgeDetailView.as_view(),
         name='user-badge-detail'),
]
