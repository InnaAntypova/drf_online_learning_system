import datetime

from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from materials.models import Course, Subscription
from materials.paginators import CustomPaginator
from materials.permissions import IsModerator, IsOwner
from materials.serializers.course import CourseSerializer
from materials.tasks import send_update_mail
from users.services import create_product, delete_product


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPaginator

    def get_permissions(self):
        """ Права доступа для ViewSet Course"""
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == 'list':
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwner]
        return super().get_permissions()

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user  # владелец
        product = create_product(new_course.title)  # создание продукта в stripe.com
        # print(product)
        new_course.pay_id = product['id']
        new_course.save()

    def perform_destroy(self, instance):
        instance = self.get_object()
        delete_product(instance.pay_id)  # удаление продукта в stripe.com
        instance.delete()

    def perform_update(self, serializer):
        course = serializer.save()
        if (timezone.now() - course.last_update) >= datetime.timedelta(hours=4):
            subscription = Subscription.objects.filter(course_id=course.pk)
            recipient_list = []
            for sub in subscription:
                recipient_list.append(sub.user.email)
            send_update_mail.delay(recipient_list, course.title)
        course.last_update = timezone.now()
        course.save()
