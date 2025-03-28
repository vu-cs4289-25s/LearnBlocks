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
#router.register(r'learnblocks', views.LearnBlocksView, 'learnblocks')

router.register(r'user',views.UserViewSet,basename='user')
#router.register(r'badge',views.BadgeViewSet,basename='badge')
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
    #path('api/', include(router.urls)),

    path('api/badges/', views.BadgeListView.as_view(), name='badge-list'),
    path('api/badges/<int:badge_id>/', views.BadgeDetailView.as_view(), name='badge-detail'),

        # Class endpoints:
    path('api/classes/', views.ClassListCreateView.as_view(), name='class-list'),
    path('api/classes/<int:class_id>/', views.ClassRetrieveUpdateDestroyView.as_view(), name='class-detail'),
    
    # ClassModuleAssignment endpoints:
    path('api/class-module-assignments/', views.ClassModuleAssignmentListCreateView.as_view(), name='classmoduleassignment-list'),
    path('api/class-module-assignments/<int:assignment_id>/', views.ClassModuleAssignmentRetrieveUpdateDestroyView.as_view(), name='classmoduleassignment-detail'),
    
    # Course endpoints:
    path('api/courses/', views.CourseListCreateView.as_view(), name='course-list'),
    path('api/courses/<int:course_id>/', views.CourseRetrieveUpdateDestroyView.as_view(), name='course-detail'),
    
    # CourseClassMapping endpoints:
    path('api/course-class-mappings/', views.CourseClassMappingListCreateView.as_view(), name='courseclassmapping-list'),
    # Here we use the course field (assumed integer) as lookup:
    path('api/course-class-mappings/<int:course>/', views.CourseClassMappingRetrieveUpdateDestroyView.as_view(), name='courseclassmapping-detail'),
    
    # Module endpoints:
    path('api/modules/', views.ModuleListCreateView.as_view(), name='module-list'),
    path('api/modules/<int:module_id>/', views.ModuleRetrieveUpdateDestroyView.as_view(), name='module-detail'),
    
    # ModuleCourseMapping endpoints:
    path('api/module-course-mappings/', views.ModuleCourseMappingListCreateView.as_view(), name='modulecoursemapping-list'),
    path('api/module-course-mappings/<int:course>/', views.ModuleCourseMappingRetrieveUpdateDestroyView.as_view(), name='modulecoursemapping-detail'),
    
    # Project endpoints:
    path('api/projects/', views.ProjectListCreateView.as_view(), name='project-list'),
    path('api/projects/<int:project_id>/', views.ProjectRetrieveUpdateDestroyView.as_view(), name='project-detail'),
    
    # User endpoints:
    path('api/users/', views.UserListCreateView.as_view(), name='user-list'),
    path('api/users/<int:user_id>/', views.UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),
    
    # UserBadgeAchievement endpoints:
    path('api/user-badge-achievements/', views.UserBadgeAchievementListCreateView.as_view(), name='userbadgeachievement-list'),
    path('api/user-badge-achievements/<int:achievement_id>/', views.UserBadgeAchievementRetrieveUpdateDestroyView.as_view(), name='userbadgeachievement-detail'),
    
    # UserClassRoster endpoints:
    path('api/user-class-rosters/', views.UserClassRosterListCreateView.as_view(), name='userclassroster-list'),
    path('api/user-class-rosters/<int:user>/', views.UserClassRosterRetrieveUpdateDestroyView.as_view(), name='userclassroster-detail'),
    
    # UserCourseEnrollment endpoints:
    path('api/user-course-enrollments/', views.UserCourseEnrollmentListCreateView.as_view(), name='usercourseenrollment-list'),
    path('api/user-course-enrollments/<int:user>/', views.UserCourseEnrollmentRetrieveUpdateDestroyView.as_view(), name='usercourseenrollment-detail'),
    
    # UserModuleProgress endpoints:
    path('api/user-module-progresses/', views.UserModuleProgressListCreateView.as_view(), name='usermoduleprogress-list'),
    path('api/user-module-progresses/<int:progress_id>/', views.UserModuleProgressRetrieveUpdateDestroyView.as_view(), name='usermoduleprogress-detail'),


    # Project associated to specific user
    path('api/projects/user/<int:userid>/', views.UserProjectsListView.as_view(), name='user_projects_list'),

    # Badges specific user
    path('api/badges/user/<int:userid>/', views.UserBadgesListView.as_view(), name='user_badges_list'),

    # Courses search by owner
    path('api/courses/user/<int:ownerid>/', views.UserCoursesListView.as_view(), name='user_courses_list'),
    
    # Courses search by class
    path('api/courses/class/<int:classid>/', views.ClassCoursesListView.as_view(), name='class_courses_list'),

    # Modules search by owner
    path('api/modules/user/<int:ownerid>/', views.UserModulesListView.as_view(), name='user_modules_list'),

]
