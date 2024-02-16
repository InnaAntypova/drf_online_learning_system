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
            {'title': 'Python', 'description': 'Изучение языка программирования Python с нуля.'},
            {'title': 'SQL', 'description': 'Основы и методы использования SQL.'}
        ]

        fill_course = []
        for course in course_list:
            fill_course.append(Course(**course))

        Course.objects.all().bulk_create(fill_course)

        # Лист с Уроками
        lessons_list = [
            {'title': 'Введение', 'description': 'Введение в основы программирования. Синтаксис. Функции. Циклы.',
             'course_id': 1},
            {'title': 'Основы веб-разработки', 'description': 'Знакомство с Linux, командной строкой. Git',
             'course_id': 1},
            {'title': 'Работа с БД', 'description': 'Базовые SQL-запросы.', 'course_id': 2},
            {'title': 'DDL', 'description': 'Нормализация таблиц', 'course_id': 2},
        ]

        fill_lessons = []
        for lesson in lessons_list:
            fill_lessons.append(Lesson(**lesson))
        Lesson.objects.all().bulk_create(fill_lessons)
