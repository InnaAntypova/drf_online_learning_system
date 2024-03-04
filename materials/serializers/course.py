from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.serializers.lesson import LessonSerializer


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()  # счетчик уроков в курсе
    lessons_in_course = serializers.SerializerMethodField()  # уроки в курсе
    subscription = serializers.SerializerMethodField()  # подписка на курс

    def get_lessons_count(self, instance):
        """ Метод для подсчета кол-ва уроков в курсе."""
        return instance.name_course.all().count()

    def get_lessons_in_course(self, instance):
        """ Метод для вывода уроков курса."""
        return LessonSerializer(Lesson.objects.filter(course=instance), many=True).data

    def get_subscription(self, instance):
        """ Метод для получения подписки на курс (True/False)"""
        request = self.context.get('request')
        # print(request.user)
        return Subscription.objects.filter(course=instance, user=request.user).exists()

    class Meta:
        model = Course
        fields = '__all__'
