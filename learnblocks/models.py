﻿# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.core.exceptions import ValidationError
from django.db import models
from .enums import enums
import uuid


class User(models.Model):
    username = models.CharField(unique=True, max_length=50)
    email = models.CharField(unique=True, max_length=255)
    password_hash = models.TextField()

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    week_activity = models.BinaryField(max_length=1, default=[0])
    role = models.TextField(choices=enums.UserRole,
                            default=enums.UserRole.STUDENT)

    class_enrollments = models.ManyToManyField(to='Class',
                                               through='UserClassRoster',
                                               related_name='users',
                                               related_query_name='user')
    badges = models.ManyToManyField(to='Badge',
                                    through='UserBadgeAchievement',
                                    related_name='users',
                                    related_query_name='user')
    course_enrollments = models.ManyToManyField(to='Course',
                                                through='UserCourseEnrollment',
                                                related_name='users',
                                                related_query_name='user')
    module_progressions = models.ManyToManyField(to='Module',
                                                 through='UserModuleProgress',
                                                 related_name='users',
                                                 related_query_name='user')

    class Meta:
        db_table = 'user'


class Class(models.Model):
    class_id = models.UUIDField(default=uuid.uuid4,
                                editable=False, unique=True)
    class_name = models.CharField(max_length=255)
    class_code = models.CharField(unique=True, max_length=20)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    courses = models.ManyToManyField(to='Course', through='ClassCourseMapping',
                                     related_name='classes',
                                     related_query_name='class')
    modules = models.ManyToManyField(to='Module',
                                     through='ClassModuleAssignment',
                                     related_name='classes',
                                     related_query_name='class')

    class Meta:
        db_table = 'class'


class Badge(models.Model):
    badge_id = models.UUIDField(default=uuid.uuid4,
                                editable=False, unique=True)

    badge_name = models.CharField(max_length=50)
    badge_description = models.TextField()
    s3_url = models.URLField()

    class Meta:
        db_table = 'badge'


class Course(models.Model):
    course_id = models.UUIDField(default=uuid.uuid4,
                                 editable=False, unique=True)
    course_name = models.CharField(max_length=255)
    status = models.TextField(choices=enums.CourseStatus,
                              default=enums.CourseStatus.ACTIVE)
    badge = models.ForeignKey(to=Badge, on_delete=models.SET_NULL, null=True,
                              related_name='badges', related_query_name='badge')
    owner = models.ForeignKey(to='User', on_delete=models.CASCADE, null=True,
                              related_name='owned_courses',
                              related_query_name='owned_course')
    visibility = models.TextField(choices=enums.CourseVisibility,
                                  default=enums.CourseVisibility.PRIVATE)

    modules = models.ManyToManyField(to='Module',
                                     through='CourseModuleMapping',
                                     related_name='courses')

    class Meta:
        db_table = 'course'


class Module(models.Model):
    module_id = models.UUIDField(default=uuid.uuid4,
                                 editable=False, unique=True)
    module_name = models.CharField(max_length=255)
    visibility = models.TextField(choices=enums.ModuleVisibility,
                                  default=enums.ModuleVisibility.PRIVATE)
    owner = models.ForeignKey(to='User', on_delete=models.CASCADE, null=True,
                              related_name='owned_modules',
                              related_query_name='owned_module')
    s3_url = models.TextField()

    class Meta:
        db_table = 'module'


class Project(models.Model):
    project_id = models.UUIDField(default=uuid.uuid4,
                                  editable=False, unique=True)
    project_name = models.CharField(max_length=100)
    s3_url = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(to='User',
                             on_delete=models.CASCADE,
                             related_name='projects',
                             related_query_name='project')
    module = models.ForeignKey(to=Module,
                               on_delete=models.SET_NULL,
                               null=True,
                               related_name='projects',
                               related_query_name='project')

    class Meta:
        db_table = 'project'


class ClassModuleAssignment(models.Model):
    assignment_id = models.UUIDField(default=uuid.uuid4,
                                     editable=False, unique=True)
    class_field = models.ForeignKey(to=Class, on_delete=models.CASCADE,
                                    db_column='class_id')
    module = models.ForeignKey(to='Module', on_delete=models.CASCADE)
    assigned_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'class_module_assignment'
        constraints = [
            models.UniqueConstraint(
                fields=('class_field', 'module'),
                name='unique_class_module')
        ]


class ClassCourseMapping(models.Model):
    assignment_id = models.UUIDField(default=uuid.uuid4,
                                     editable=False, unique=True)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    class_field = models.ForeignKey(to=Class,
                                    on_delete=models.CASCADE,
                                    db_column='class_id')
    assigned_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'class_course_mapping'
        constraints = [
            models.UniqueConstraint(
                fields=('course', 'class_field'),
                name='unique_course_class')
        ]


class CourseModuleMapping(models.Model):
    entry_id = models.UUIDField(default=uuid.uuid4,
                                editable=False, unique=True)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    module = models.ForeignKey(to=Module, on_delete=models.CASCADE)
    module_order = models.IntegerField()

    def save(self, *args, **kwargs):
        if self.module_order < 0:
            raise ValidationError("module_order must be positive")
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'course_module_mapping'
        constraints = [
            models.UniqueConstraint(
                fields=('course', 'module'),
                name='unique_course_module')
        ]


class UserBadgeAchievement(models.Model):
    achievement_id = models.UUIDField(default=uuid.uuid4,
                                      editable=False, unique=True)
    badge = models.ForeignKey(to=Badge, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    earned_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_badge_achievement'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'badge'),
                name='unique_user_badge')
        ]


class UserClassRoster(models.Model):
    # The composite primary key (user_id, class_id) found,
    # that is not supported. The first column is selected.
    entry_id = models.UUIDField(default=uuid.uuid4,
                                editable=False, unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    class_field = models.ForeignKey(to=Class, on_delete=models.CASCADE,
                                    db_column='class_id')
    role = models.TextField(choices=enums.RosterRole,
                            default=enums.RosterRole.PARTICIPANT)
    enrollment_date = models.DateField()

    class Meta:
        db_table = 'user_class_roster'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'class_field'),
                name='unique_user_class')
        ]


class UserCourseEnrollment(models.Model):
    enrollment_id = models.UUIDField(default=uuid.uuid4,
                                     editable=False, unique=True)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_course_enrollment'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'course'),
                name='unique_user_course')
        ]


class UserModuleProgress(models.Model):
    progress_id = models.UUIDField(default=uuid.uuid4,
                                   editable=False, unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    module = models.ForeignKey(to=Module, on_delete=models.CASCADE)
    status = models.TextField(choices=enums.ModuleStatus,
                              default=enums.ModuleStatus.LOCKED)
    completion_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'user_module_progress'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'module'),
                name='unique_user_module')
        ]
