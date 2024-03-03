from django.core.management.base import BaseCommand
from django.core.management.color import no_style
from django.db import connection

from materials.models import Course, Lesson


class Command(BaseCommand):
    def handle(self, *args, **options):
        """ Создание тестовых курсов и уроков """
        # Удалить ранее созданные
        Lesson.objects.all().delete()
        Course.objects.all().delete()

        # Сброс PrimaryKey в таблицах
        sequence_sql = connection.ops.sequence_reset_sql(no_style(), [Lesson, Course])
        with connection.cursor() as cursor:
            for sql in sequence_sql:
                cursor.execute(sql)

        # Лист с Курсами
        course_list = [
            {'title': 'Python', 'description': 'Изучение языка программирования Python с нуля.', 'owner_id': 1},
            {'title': 'SQL', 'description': 'Основы и методы использования SQL.', 'owner_id': 1},
            {'title': 'Java', 'description': 'Научим всем ключевым навыкам Java-разработчика', 'owner_id': 1},
            {'title': 'Профессия Фронтенд-разработчик',
             'description': 'Фронтенд — всё, что мы видим на экране смартфона или компьютера', 'owner_id': 1},
            {'title': 'Инженер по тестированию',
             'description': 'Вы научитесь находить ошибки в работе сайтов и приложений с помощью Java, '
                            'JavaScript или Python.', 'owner_id': 1},
            {'title': 'Профессия Веб-разработчик',
             'description': 'Веб-разработчик создаёт сайты, сервисы и приложения, которыми мы ежедневно пользуемся.',
             'owner_id': 1}
        ]

        fill_course = []
        for course in course_list:
            fill_course.append(Course(**course))

        Course.objects.all().bulk_create(fill_course)

        # Лист с Уроками
        lessons_list = [
            {'title': 'Введение', 'description': 'Введение в основы программирования. Синтаксис. Функции. Циклы.',
             'course_id': 1, 'owner_id': 1},
            {'title': 'Основы веб-разработки', 'description': 'Знакомство с Linux, командной строкой. Git',
             'course_id': 1, 'owner_id': 1},
            {'title': 'ООП', 'description': 'Погружение в объектно-ориентированное программирование (ООП)',
             'course_id': 1, 'owner_id': 1},
            {'title': 'Работа с базами данных', 'description': 'Осваиваем базы данных',
             'course_id': 1, 'owner_id': 1},
            {'title': 'Django', 'description': 'Осваиваем Django с нуля',
             'course_id': 1, 'owner_id': 1},
            {'title': 'DRF', 'description': 'Django Rest Framework',
             'course_id': 1, 'owner_id': 1},
            {'title': 'Docker', 'description': 'Основы Docker',
             'course_id': 1, 'owner_id': 1},
            {'title': 'Работа с БД', 'description': 'Базовые SQL-запросы.', 'course_id': 2, 'owner_id': 1},
            {'title': 'DDL', 'description': 'Нормализация таблиц', 'course_id': 2, 'owner_id': 1},
        ]

        fill_lessons = []
        for lesson in lessons_list:
            fill_lessons.append(Lesson(**lesson))
        Lesson.objects.all().bulk_create(fill_lessons)
