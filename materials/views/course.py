from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from materials.models import Course
from materials.paginators import CustomPaginator
from materials.permissions import IsModerator, IsOwner
from materials.serializers.course import CourseSerializer
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
