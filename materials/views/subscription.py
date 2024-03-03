from rest_framework.generics import UpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Subscription
from materials.serializers.subscription import SubscriptionSerializer


class UserSubscriptionAPIView(APIView):
    """ Представление для управления Subscription (Подпиской) """
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course')  # получаем id курса
        # print(course_id)
        course_item = get_object_or_404(queryset=Course.objects.all(), id=course_id)  # получаем объект курса
        # print(course_item)
        subs_item = Subscription.objects.filter(user_id=user, course=course_item)  # получаем подписку
        # print(subs_item)
        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course_id=course_id)
            message = 'Подписка добавлена'
        return Response({'message': message})
