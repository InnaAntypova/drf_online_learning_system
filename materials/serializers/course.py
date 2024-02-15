from rest_framework import serializers

from materials.models import Course


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()  # счетчик уроков в курсе

    def get_lessons_count(self, instance):
        """ Метод для подсчета кол-ва уроков в курсе."""
        return instance.name_course.all().count()

    class Meta:
        model = Course
        fields = '__all__'
