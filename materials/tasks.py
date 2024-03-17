from celery import shared_task
from django.core.mail import send_mail

from config import settings


@shared_task
def send_update_mail(recipient_list, course_title: str):
    """ Отложенная задача по отправке письма об обновлении курса. """
    # print(recipient_list)
    send_mail(
        subject=f"Курс {course_title}",
        message=f"Курс {course_title} был обновлен. Посмотрите изменения.",
        from_email=settings.SERVER_EMAIL,
        recipient_list=recipient_list
    )
