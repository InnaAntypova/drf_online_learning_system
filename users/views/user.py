from rest_framework.generics import UpdateAPIView, RetrieveAPIView, CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.response import Response

from users.models import User
from users.serializers.user import UserSerializer, UserProfileSerializer, UserRegistrationSerializer


class UserUpdateAPIView(UpdateAPIView):
    """ Представление для обновления профиля User """
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserProfileAPIView(RetrieveAPIView):
    """ Представление для профиля User """
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()


class UserRegistrationAPIView(CreateAPIView):
    """ Представление для регистрации User """
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = True  # активировать пользователя
            user.save()
        return Response({'message': 'User создан успешно.'})


class UserListAPIView(ListAPIView):
    """ Представление для отображения списка Users"""
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDeleteAPIView(DestroyAPIView):
    """ Представление для удаления User """
    serializer_class = UserSerializer
    queryset = User.objects.all()
