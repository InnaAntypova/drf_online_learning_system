import uuid as uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    """ Модель для пользователя User"""

    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='Номер телефона', **NULLABLE)
    city = models.CharField(max_length=50, verbose_name='Город', **NULLABLE)

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name='UUID')

    is_active = models.BooleanField(default=False, verbose_name='Состояние активности')
    is_staff = models.BooleanField(default=False, verbose_name='Сотрудник')
    is_superuser = models.BooleanField(default=False, verbose_name='Администратор')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email} / {self.is_active}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Payment(models.Model):
    """ Модель для сущности Payment (Платежи) """
    class PaymentMethod(models.TextChoices):
        CASH = "Наличные"
        TRANSFER = "Перевод на карту"

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='user', verbose_name='Пользователь')
    pay_date = models.DateField(verbose_name='Дата оплаты')
    paid_course = models.ForeignKey('materials.Course', on_delete=models.CASCADE, related_name='paid_course',
                                    verbose_name='Оплаченный курс', **NULLABLE)
    paid_lesson = models.ForeignKey('materials.Lesson', on_delete=models.CASCADE, related_name='paid_lesson',
                                    verbose_name='Оплаченный урок', **NULLABLE)
    payment_amount = models.PositiveIntegerField(verbose_name='Сумма оплаты')
    payment_method = models.CharField(choices=PaymentMethod.choices, default=PaymentMethod.CASH,
                                      verbose_name='Способ оплаты')
