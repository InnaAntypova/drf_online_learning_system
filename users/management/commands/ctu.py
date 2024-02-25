from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        """ Создание тестового пользователя """
        test_user = User.objects.create(
            email='test@test.ru',
            is_active=True,  # активируем пользователя
        )
        test_user.set_password('12345')
        test_user.groups.add(Group.objects.get(name='MEMBER'))
        test_user.save()

