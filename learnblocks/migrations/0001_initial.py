# Generated by Django 5.1.7 on 2025-03-27 23:36

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('badge_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('badge_name', models.CharField(max_length=50)),
                ('badge_description', models.TextField()),
                ('s3_url', models.URLField()),
            ],
            options={
                'db_table': 'badge',
            },
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('class_name', models.CharField(max_length=255)),
                ('class_code', models.CharField(max_length=20, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'class',
            },
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('module_name', models.CharField(max_length=255)),
                ('visibility', models.TextField(choices=[('public', 'Public'), ('private', 'Private')], default='private')),
                ('s3_url', models.TextField()),
            ],
            options={
                'db_table': 'module',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('password_hash', models.TextField()),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('week_activity', models.BinaryField(default=[0], max_length=1)),
                ('role', models.TextField(choices=[('admin', 'Admin'), ('teacher', 'Teacher'), ('student', 'Student')], default='student')),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('course_name', models.CharField(max_length=255)),
                ('status', models.TextField(choices=[('active', 'Active'), ('archived', 'Archived')], default='active')),
                ('visibility', models.TextField(choices=[('public', 'Public'), ('private', 'Private')], default='private')),
                ('badge', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='badges', related_query_name='badge', to='learnblocks.badge')),
            ],
            options={
                'db_table': 'course',
            },
        ),
        migrations.CreateModel(
            name='ClassCourseMapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignment_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('assigned_date', models.DateTimeField(auto_now_add=True)),
                ('class_field', models.ForeignKey(db_column='class_id', on_delete=django.db.models.deletion.CASCADE, to='learnblocks.class')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learnblocks.course')),
            ],
            options={
                'db_table': 'class_course_mapping',
            },
        ),
        migrations.AddField(
            model_name='class',
            name='courses',
            field=models.ManyToManyField(related_name='classes', related_query_name='class', through='learnblocks.ClassCourseMapping', to='learnblocks.course'),
        ),
        migrations.CreateModel(
            name='CourseModuleMapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('module_order', models.IntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learnblocks.course')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learnblocks.module')),
            ],
            options={
                'db_table': 'course_module_mapping',
            },
        ),
        migrations.AddField(
            model_name='course',
            name='modules',
            field=models.ManyToManyField(related_name='courses', through='learnblocks.CourseModuleMapping', to='learnblocks.module'),
        ),
        migrations.CreateModel(
            name='ClassModuleAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignment_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('assigned_date', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('class_field', models.ForeignKey(db_column='class_id', on_delete=django.db.models.deletion.CASCADE, to='learnblocks.class')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learnblocks.module')),
            ],
            options={
                'db_table': 'class_module_assignment',
            },
        ),
        migrations.AddField(
            model_name='class',
            name='modules',
            field=models.ManyToManyField(related_name='classes', related_query_name='class', through='learnblocks.ClassModuleAssignment', to='learnblocks.module'),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('project_name', models.CharField(max_length=100)),
                ('s3_url', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('module', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projects', related_query_name='project', to='learnblocks.module')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', related_query_name='project', to='learnblocks.user')),
            ],
            options={
                'db_table': 'project',
            },
        ),
        migrations.AddField(
            model_name='module',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owned_modules', related_query_name='owned_module', to='learnblocks.user'),
        ),
        migrations.AddField(
            model_name='course',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owned_courses', related_query_name='owned_course', to='learnblocks.user'),
        ),
        migrations.CreateModel(
            name='UserBadgeAchievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('achievement_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('earned_date', models.DateTimeField(auto_now_add=True)),
                ('badge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learnblocks.badge')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learnblocks.user')),
            ],
            options={
                'db_table': 'user_badge_achievement',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='badges',
            field=models.ManyToManyField(related_name='users', related_query_name='user', through='learnblocks.UserBadgeAchievement', to='learnblocks.badge'),
        ),
        migrations.CreateModel(
            name='UserClassRoster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('role', models.TextField(choices=[('owner', 'Owner'), ('participant', 'Participant')], default='participant')),
                ('enrollment_date', models.DateField()),
                ('class_field', models.ForeignKey(db_column='class_id', on_delete=django.db.models.deletion.CASCADE, to='learnblocks.class')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learnblocks.user')),
            ],
            options={
                'db_table': 'user_class_roster',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='class_enrollments',
            field=models.ManyToManyField(related_name='users', related_query_name='user', through='learnblocks.UserClassRoster', to='learnblocks.class'),
        ),
        migrations.CreateModel(
            name='UserCourseEnrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrollment_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learnblocks.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learnblocks.user')),
            ],
            options={
                'db_table': 'user_course_enrollment',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='course_enrollments',
            field=models.ManyToManyField(related_name='users', related_query_name='user', through='learnblocks.UserCourseEnrollment', to='learnblocks.course'),
        ),
        migrations.CreateModel(
            name='UserModuleProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('status', models.TextField(choices=[('locked', 'Locked'), ('in_progress', 'Inprogress'), ('completed', 'Completed')], default='locked')),
                ('completion_date', models.DateTimeField(null=True)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learnblocks.module')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learnblocks.user')),
            ],
            options={
                'db_table': 'user_module_progress',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='module_progressions',
            field=models.ManyToManyField(related_name='users', related_query_name='user', through='learnblocks.UserModuleProgress', to='learnblocks.module'),
        ),
        migrations.AddConstraint(
            model_name='classcoursemapping',
            constraint=models.UniqueConstraint(fields=('course', 'class_field'), name='unique_course_class'),
        ),
        migrations.AddConstraint(
            model_name='coursemodulemapping',
            constraint=models.UniqueConstraint(fields=('course', 'module'), name='unique_course_module'),
        ),
        migrations.AddConstraint(
            model_name='classmoduleassignment',
            constraint=models.UniqueConstraint(fields=('class_field', 'module'), name='unique_class_module'),
        ),
        migrations.AddConstraint(
            model_name='userbadgeachievement',
            constraint=models.UniqueConstraint(fields=('user', 'badge'), name='unique_user_badge'),
        ),
        migrations.AddConstraint(
            model_name='userclassroster',
            constraint=models.UniqueConstraint(fields=('user', 'class_field'), name='unique_user_class'),
        ),
        migrations.AddConstraint(
            model_name='usercourseenrollment',
            constraint=models.UniqueConstraint(fields=('user', 'course'), name='unique_user_course'),
        ),
        migrations.AddConstraint(
            model_name='usermoduleprogress',
            constraint=models.UniqueConstraint(fields=('user', 'module'), name='unique_user_module'),
        ),
    ]
