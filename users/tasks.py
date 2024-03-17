from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def deactivate_user():
    """ Периодическая задача по деактивации неактивных пользователей """
    check_date = timezone.now() - timedelta(days=30)
    # print(check_date)
    users = User.objects.filter(is_active=True)
    users_ = users.filter(last_login__lte=check_date)  # последний вход меньше или равно проверочной дате
    # print(users_)
    users_.update(is_active=False)




