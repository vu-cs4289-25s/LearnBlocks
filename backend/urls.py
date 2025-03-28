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
from learnblocks import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('badges/', views.BadgeListView.as_view(), name='badge-list'),
    path('badges/<uuid:badge_id>/',
         views.BadgeDetailView.as_view(), name='badge-detail'),

    # Class endpoints:
    path('classes/', views.ClassListCreateView.as_view(), name='class-list'),
    path('classes/<uuid:class_id>/',
         views.ClassRetrieveUpdateDestroyView.as_view(), name='class-detail'),

    # ClassModuleAssignment endpoints:
    path('class-module-assignments/', views.ClassModuleAssignmentListCreateView.as_view(),
         name='classmoduleassignment-list'),
    path('class-module-assignments/<uuid:assignment_id>/',
         views.ClassModuleAssignmentRetrieveUpdateDestroyView.as_view(), name='classmoduleassignment-detail'),

    # Course endpoints:
    path('courses/', views.CourseListCreateView.as_view(), name='course-list'),
    path('courses/<uuid:course_id>/',
         views.CourseRetrieveUpdateDestroyView.as_view(), name='course-detail'),

    # CourseClassMapping endpoints:
    path('course-class-mappings/', views.ClassCourseMappingListCreateView.as_view(),
         name='courseclassmapping-list'),
    # Here we use the course field (assumed integer) as lookup:
    path('course-class-mappings/<uuid:course>/',
         views.ClassCourseMappingRetrieveUpdateDestroyView.as_view(), name='courseclassmapping-detail'),

    # Module endpoints:
    path('modules/', views.ModuleListCreateView.as_view(), name='module-list'),
    path('modules/<uuid:module_id>/',
         views.ModuleRetrieveUpdateDestroyView.as_view(), name='module-detail'),

    # ModuleCourseMapping endpoints:
    path('module-course-mappings/', views.CourseModuleMappingListCreateView.as_view(),
         name='modulecoursemapping-list'),
    path('module-course-mappings/<uuid:course>/',
         views.CourseModuleMappingRetrieveUpdateDestroyView.as_view(), name='modulecoursemapping-detail'),

    # Project endpoints:
    path('projects/', views.ProjectListCreateView.as_view(), name='project-list'),
    path('projects/<uuid:project_id>/',
         views.ProjectRetrieveUpdateDestroyView.as_view(), name='project-detail'),

    # User endpoints:
    path('users/', views.UserListCreateView.as_view(), name='user-list'),
    path('users/<uuid:user_id>/',
         views.UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),

    # UserBadgeAchievement endpoints:
    path('user-badge-achievements/', views.UserBadgeAchievementListCreateView.as_view(),
         name='userbadgeachievement-list'),
    path('user-badge-achievements/<uuid:achievement_id>/',
         views.UserBadgeAchievementRetrieveUpdateDestroyView.as_view(), name='userbadgeachievement-detail'),

    # UserClassRoster endpoints:
    path('user-class-rosters/', views.UserClassRosterListCreateView.as_view(),
         name='userclassroster-list'),
    path('user-class-rosters/<string:username>/',
         views.UserClassRosterRetrieveUpdateDestroyView.as_view(), name='userclassroster-detail'),

    # UserCourseEnrollment endpoints:
    path('user-course-enrollments/', views.UserCourseEnrollmentListCreateView.as_view(),
         name='usercourseenrollment-list'),
    path('user-course-enrollments/<string:username>/',
         views.UserCourseEnrollmentRetrieveUpdateDestroyView.as_view(), name='usercourseenrollment-detail'),

    # UserModuleProgress endpoints:
    path('user-module-progresses/', views.UserModuleProgressListCreateView.as_view(),
         name='usermoduleprogress-list'),
    path('user-module-progresses/<uuid:progress_id>/',
         views.UserModuleProgressRetrieveUpdateDestroyView.as_view(), name='usermoduleprogress-detail'),
]
