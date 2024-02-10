from rest_framework.viewsets import ModelViewSet
from materials.models import Course
from materials.serializers.course import CourseSerializer


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

