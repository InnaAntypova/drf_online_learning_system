import uuid as uuid

from django.apps import apps
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

NULLABLE = {'null': True, 'blank': True}


class UserManager(BaseUserManager):
    """ Менеджер для модели User. """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        email = GlobalUserModel.normalize_username(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """ Модель для пользователя User"""
    objects = UserManager()

    # class UserRole(models.TextChoices):
    #     MEMBER = 'member', _('member')
    #     MODERATOR = 'moderator', _('moderator')

    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='Номер телефона', **NULLABLE)
    city = models.CharField(max_length=50, verbose_name='Город', **NULLABLE)

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name='UUID')

    is_active = models.BooleanField(default=False, verbose_name='Состояние активности')
    is_staff = models.BooleanField(default=False, verbose_name='Сотрудник')
    is_superuser = models.BooleanField(default=False, verbose_name='Администратор')

    # role = models.CharField(max_length=9, choices=UserRole.choices, default=UserRole.MEMBER)

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
