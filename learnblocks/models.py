# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Badge(models.Model):
    badge_id = models.AutoField(primary_key=True)
    badge_name = models.CharField(max_length=50)
    badge_description = models.TextField()
    s3_url = models.TextField()

    class Meta:
        managed = False
        db_table = 'badge'


class Class(models.Model):
    class_id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=255)
    class_code = models.CharField(unique=True, max_length=20)
    is_active = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'class'


class ClassModuleAssignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    class_field = models.ForeignKey(Class, models.CASCADE, db_column='class_id', blank=True, null=True)  # Field renamed because it was a Python reserved word.
    module = models.ForeignKey('Module', models.CASCADE, blank=True, null=True)
    assigned_date = models.DateTimeField(blank=True, null=True)
    due_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'class_module_assignment'


class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    status = models.TextField(blank=True, null=True)  # This field type is a guess.
    badge = models.ForeignKey(Badge, models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey('User', models.CASCADE, blank=True, null=True)
    permission = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'course'


class CourseClassMapping(models.Model):
    course = models.OneToOneField(Course, models.CASCADE, primary_key=True)  # The composite primary key (course_id, class_id) found, that is not supported. The first column is selected.
    class_field = models.ForeignKey(Class, models.CASCADE, db_column='class_id')  # Field renamed because it was a Python reserved word.
    assigned_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course_class_mapping'
        unique_together = (('course', 'class_field'),)


class Module(models.Model):
    module_id = models.AutoField(primary_key=True)
    module_name = models.CharField(max_length=255)
    status = models.TextField(blank=True, null=True)  # This field type is a guess.
    owner = models.ForeignKey('User', models.CASCADE, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'module'


class ModuleCourseMapping(models.Model):
    course = models.OneToOneField(Course, models.CASCADE, primary_key=True)  # The composite primary key (course_id, module_id) found, that is not supported. The first column is selected.
    module = models.ForeignKey(Module, models.CASCADE)
    module_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'module_course_mapping'
        unique_together = (('course', 'module'),)


class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', models.CASCADE, blank=True, null=True)
    project_name = models.CharField(max_length=100)
    module = models.ForeignKey(Module, models.CASCADE, blank=True, null=True)
    s3_url = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    last_modified = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project'


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    role = models.TextField()  # This field type is a guess.
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(unique=True, max_length=50)
    email = models.CharField(unique=True, max_length=255)
    password_hash = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    week_activity = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'user'


class UserBadgeAchievement(models.Model):
    achievement_id = models.AutoField(primary_key=True)
    badge = models.ForeignKey(Badge, models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, models.CASCADE, blank=True, null=True)
    earned_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_badge_achievement'


class UserClassRoster(models.Model):
    user = models.OneToOneField(User, models.CASCADE, primary_key=True)  # The composite primary key (user_id, class_id) found, that is not supported. The first column is selected.
    class_field = models.ForeignKey(Class, models.CASCADE, db_column='class_id')  # Field renamed because it was a Python reserved word.
    role = models.TextField()  # This field type is a guess.
    enrollment_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_class_roster'
        unique_together = (('user', 'class_field'),)


class UserCourseEnrollment(models.Model):
    course = models.ForeignKey(Course, models.CASCADE)
    user = models.OneToOneField(User, models.CASCADE, primary_key=True)  # The composite primary key (user_id, course_id) found, that is not supported. The first column is selected.
    role = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'user_course_enrollment'
        unique_together = (('user', 'course'),)


class UserModuleProgress(models.Model):
    progress_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.CASCADE, blank=True, null=True)
    module = models.ForeignKey(Module, models.CASCADE, blank=True, null=True)
    status = models.TextField(blank=True, null=True)  # This field type is a guess.
    completion_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_module_progress'
