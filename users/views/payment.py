from rest_framework.generics import ListAPIView

from users.models import Payment
from users.serializers.payment import PaymentSerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class PaymentListAPIView(ListAPIView):
    """ Представление для списка платежей """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')
    ordering_fields = ('pay_date',)

