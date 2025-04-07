from django.contrib import admin
from .models import (
    Badge, User, Class, Course, Module, Project,
    ClassCourseMapping, ClassModuleAssignment, CourseModuleMapping,
    UserBadgeAchievement, UserClassRoster,
    UserCourseEnrollment, UserModuleProgress)

# Optional: custom ModelAdmins for better display


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'created_at')
    search_fields = ('username', 'email')
    list_filter = ('role',)


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'status', 'owner', 'visibility')
    list_filter = ('status', 'visibility')
    search_fields = ('course_name',)


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'join_code', 'is_active')
    search_fields = ('class_name',)
    list_filter = ('is_active',)


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('module_name', 'visibility', 'owner')
    search_fields = ('module_name',)
    list_filter = ('visibility',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'owner', 'module',
                    'created_at', 'last_modified')
    search_fields = ('project_name',)
    list_filter = ('created_at', 'last_modified')


# Simpler registrations for join tables
admin.site.register(ClassCourseMapping)
admin.site.register(ClassModuleAssignment)
admin.site.register(CourseModuleMapping)
admin.site.register(UserBadgeAchievement)
admin.site.register(UserClassRoster)
admin.site.register(UserCourseEnrollment)
admin.site.register(UserModuleProgress)
