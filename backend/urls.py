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
         views.ClassRetrieveUpdateDestroyView.as_view(),
         name='class-detail'),

    # ClassModuleAssignment endpoints:
    path('classes/<uuid:class_id>/modules/',
         views.ClassModuleAssignmentListCreateView.as_view(),
         name='class-modules-list'),
    path('classes/<uuid:class_id>/modules/<uuid:module_id>/',
         views.ClassModuleAssignmentRetrieveUpdateDestroyView.as_view(),
         name='class-modules-detail'),

    # ClassCourseMapping endpoints:
    path('classes/<uuid:class_id>/courses/',
         views.ClassCourseMappingListCreateView.as_view(),
         name='class-courses-list'),
    path('classes/<uuid:class_id>/courses/<uuid:course_id>/',
         views.ClassCourseMappingRetrieveUpdateDestroyView.as_view(),
         name='class-courses-detail'),

    # Course endpoints:
    path('courses/', views.CourseListCreateView.as_view(),
         name='course-list'),
    path('courses/<uuid:course_id>/',
         views.CourseRetrieveUpdateDestroyView.as_view(),
         name='course-detail'),

    # CourseModuleMapping endpoints:
    path('courses/<uuid:course_id>/modules/',
         views.CourseModuleMappingListCreateView.as_view(),
         name='course-modules-list'),
    path('courses/<uuid:course_id>/modules/<uuid:module_id>/',
         views.CourseModuleMappingRetrieveUpdateDestroyView.as_view(),
         name='course-modules-detail'),

    # Module endpoints:
    path('modules/', views.ModuleListCreateView.as_view(), name='module-list'),
    path('modules/<uuid:module_id>/',
         views.ModuleRetrieveUpdateDestroyView.as_view(),
         name='module-detail'),

    # Project endpoints:
    path('projects/', views.ProjectListCreateView.as_view(),
         name='project-list'),
    path('projects/<uuid:project_id>/',
         views.ProjectRetrieveUpdateDestroyView.as_view(),
         name='project-detail'),

    # User endpoints:
    path('users/', views.UserListCreateView.as_view(), name='user-list'),
    path('users/<uuid:user_id>/',
         views.UserRetrieveUpdateDestroyView.as_view(),
         name='user-detail'),
    path('users/<uuid:user_id>/projects',
         views.UserProjectsListView.as_view(),
         name='user_projects_list'),
    path('users/<uuid:user_id>/badges',
         views.UserBadgesListView.as_view(),
         name='user_badges_list'),
    path('users/<uuid:user_id>/courses',
         views.UserCoursesListView.as_view(),
         name='user_courses_list'),
    path('users/<uuid:user_id>/modules',
         views.UserModulesListView.as_view(),
         name='user_modules_list'),

    # UserBadgeAchievement endpoints:
    path('user-badge-achievements/',
         views.UserBadgeAchievementListCreateView.as_view(),
         name='userbadgeachievement-list'),
    path('user-badge-achievements/<uuid:achievement_id>/',
         views.UserBadgeAchievementRetrieveUpdateDestroyView.as_view(),
         name='userbadgeachievement-detail'),

    # UserClassRoster endpoints:
    path('user-class-rosters/', views.UserClassRosterListCreateView.as_view(),
         name='userclassroster-list'),
    path('user-class-rosters/<str:username>/',
         views.UserClassRosterRetrieveUpdateDestroyView.as_view(),
         name='userclassroster-detail'),

    # UserCourseEnrollment endpoints:
    path('user-course-enrollments/',
         views.UserCourseEnrollmentListCreateView.as_view(),
         name='usercourseenrollment-list'),
    path('user-course-enrollments/<str:username>/',
         views.UserCourseEnrollmentRetrieveUpdateDestroyView.as_view(),
         name='usercourseenrollment-detail'),

    # UserModuleProgress endpoints:
    path('user-module-progresses/',
         views.UserModuleProgressListCreateView.as_view(),
         name='usermoduleprogress-list'),
    path('user-module-progresses/<uuid:progress_id>/',
         views.UserModuleProgressRetrieveUpdateDestroyView.as_view(),
         name='usermoduleprogress-detail'),
]
