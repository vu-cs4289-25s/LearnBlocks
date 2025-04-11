from django.db.models.signals import post_save
from django.db.models import Count, Q, F
from django.dispatch import receiver
from .models import UserModuleProgress, CourseModuleMapping, Course, UserBadgeAchievement
from .enums import ModuleStatus


@receiver(post_save, sender=UserModuleProgress)
def check_course_completion(sender, instance: UserModuleProgress, **kwargs):
    user = instance.user
    module = instance.module
    course_ids = CourseModuleMapping.objects.filter(module=module
                                                    ).values_list('course',
                                                                  flat=True)
    courses = Course.objects.filter(course_id__in=course_ids)

    annotated_courses = courses.annotate(
        total_modules=Count('modules', distinct=True),
        completed_modules=Count(
            'modules',
            filter=Q(modules__usermoduleprogress__status=ModuleStatus.COMPLETED,
                     modules__usermoduleprogress__user=user), distinct=True))

    complete_courses = annotated_courses.filter(total_modules=F('completed_modules'),
                                                total_modules__gt=0)

    for course in complete_courses:
        if course.badge:
            badge, created = UserBadgeAchievement.objects.get_or_create(
                badge=course.badge, user=user)
            if created:
                print(f"Awarded badge {badge.badge} to {user.username}")
