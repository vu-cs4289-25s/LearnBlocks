from django.db import models


class UserRole(models.TextChoices):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"


class RosterRole(models.TextChoices):
    OWNER = "owner"
    PARTICIPANT = "participant"


class CourseRole(models.TextChoices):
    OWNER = "owner"
    PARTICIPANT = "participant"


class TaskStatus(models.TextChoices):
    ASSIGNED = "assigned"
    INPROGRESS = "in_progress"
    COMPLETED = "completed"


class ModuleStatus(models.TextChoices):
    LOCKED = "locked"
    INPROGRESS = "in_progress"
    COMPLETED = "completed"


class ModuleVisibility(models.TextChoices):
    PUBLIC = "public"
    PRIVATE = "private"


class CourseStatus(models.TextChoices):
    ACTIVE = "active"
    ARCHIVED = "archived"


class CourseVisibility(models.TextChoices):
    PUBLIC = "public"
    PRIVATE = "private"
