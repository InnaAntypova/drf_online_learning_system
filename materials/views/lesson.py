from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView

from materials.models import Lesson
from materials.serializers.lesson import LessonSerializer


class LessonListAPIView(ListAPIView):
    """ Представление для просмотра всех объектов """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonCreateAPIView(CreateAPIView):
    """ Представление для создания нового объекта """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(UpdateAPIView):
    """" Представление для обновления объекта """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(RetrieveAPIView):
    """ Представление для деталей одного объекта """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDeleteAPIView(DestroyAPIView):
    """ Представление для удаления объекта """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
