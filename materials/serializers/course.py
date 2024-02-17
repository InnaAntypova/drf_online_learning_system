from rest_framework import serializers

from materials.models import Course, Lesson
from materials.serializers.lesson import LessonSerializer


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()  # счетчик уроков в курсе
    lessons_in_course = serializers.SerializerMethodField()  # уроки в курсе

    def get_lessons_count(self, instance):
        """ Метод для подсчета кол-ва уроков в курсе."""
        return instance.name_course.all().count()

    def get_lessons_in_course(self, instance):
        """ Метод для вывода уроков курса."""
        return LessonSerializer(Lesson.objects.filter(course=instance), many=True).data

    class Meta:
        model = Course
        fields = '__all__'
