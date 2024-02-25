from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        member_group, created = Group.objects.get_or_create(name='MEMBER')
        if created:
            permissions = Permission.objects.filter(
                codename__in=['add_course', 'change_course', 'delete_course', 'view_course', 'add_lesson',
                              'change_lesson', 'delete_lesson', 'view_lesson']
            )
            member_group.permissions.set(permissions)

        moderator_group, created = Group.objects.get_or_create(name='MODERATOR')
        if created:
            permissions = Permission.objects.filter(
                codename__in=['change_course', 'view_course', 'change_lesson', 'view_lesson']
            )
            moderator_group.permissions.set(permissions)
