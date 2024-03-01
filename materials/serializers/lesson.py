from rest_framework import serializers

from materials.models import Lesson
from materials.validators import URLValidator


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [URLValidator(field='description'), URLValidator(field='video_url')]
