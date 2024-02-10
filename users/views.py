from rest_framework.generics import UpdateAPIView

from users.models import User
from users.serializers import UserSerializer


class UserUpdateAPIView(UpdateAPIView):
    """ Представление для обновления профиля User """
    serializer_class = UserSerializer
    queryset = User.objects.all()
