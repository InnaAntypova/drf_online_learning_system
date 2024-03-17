from django.db import models

from config import settings

NULLABLE = {'null': True, 'blank': True}


class Course(models.Model):
    """ Модель для сущности Course (Курс) """
    title = models.CharField(max_length=150, verbose_name='Название')
    image = models.ImageField(upload_to='course.py/', verbose_name='Превью (картинка)', **NULLABLE)
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    amount = models.PositiveIntegerField(verbose_name='Стоимость', **NULLABLE)
    last_update = models.DateTimeField(auto_now_add=True, verbose_name='Последнее обновление', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец')

    pay_id = models.CharField(verbose_name='ID для платежей', **NULLABLE)

    def __str__(self):
        return f'{self.title}/{self.owner}/{self.pay_id}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    """ Модель для сущности Lesson (Урок) """
    title = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    image = models.ImageField(upload_to='lesson/', verbose_name='Превью (картинка)', **NULLABLE)
    video_url = models.URLField(verbose_name='Ссылка на видео', **NULLABLE)

    course = models.ForeignKey('materials.Course', related_name='name_course', on_delete=models.CASCADE,
                               verbose_name='Курс')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец')

    def __str__(self):
        return f'{self.title} / {self.course}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Subscription(models.Model):
    """ Модель для сущности Subscription (Подписка) """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    course = models.ForeignKey('materials.Course', related_name='sub_course', on_delete=models.CASCADE,
                               verbose_name='Курс')

    def __str__(self):
        return f'{self.user}/{self.course}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
