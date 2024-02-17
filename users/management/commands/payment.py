from django.core.management.base import BaseCommand

from users.models import Payment


class Command(BaseCommand):
    def handle(self, *args, **options):
        """ Тестовые данные для Payment """
    test_payment_1 = Payment.objects.create(
        user_id=1,
        pay_date='2024-02-16',
        paid_course_id=1,
        payment_amount=25000,
        payment_method=Payment.PaymentMethod.CASH
    )

    test_payment_2 = Payment.objects.create(
        user_id=1,
        pay_date='2024-02-17',
        paid_lesson_id=3,
        payment_amount=5000,
        payment_method=Payment.PaymentMethod.TRANSFER
    )

