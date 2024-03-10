
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Payment
from users.serializers.payment import PaymentSerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from users.services import create_payment, get_status


class PaymentListAPIView(ListAPIView):
    """ Представление для списка платежей """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')
    ordering_fields = ('pay_date',)


class PaymentCreateAPIView(CreateAPIView):
    """ Представление для создания платежа """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        course = serializer.validated_data.get('paid_course')
        if course and course.amount is not None:
            new_payment = serializer.save()
            session = create_payment(course.amount, course.pay_id, self.request.user.email)
            new_payment.payment_id = session['id']
            new_payment.payment_url = session['url']
            new_payment.save()
        else:
            raise serializer.ValidationError('Не выбран курс!')


class PaymentStatusAPIView(APIView):
    """ Представление для получения статуса платежа """
    serializer_class = PaymentSerializer

    def get(self, request, pk):
        payment = Payment.objects.get(pk=pk)
        status = get_status(payment.payment_id)
        print(status)
        if status == 'paid':
            message = 'Платеж оплачен.'
            payment.payment_status = payment.PaymentStatus.PAID
        if status == 'unpaid':
            message = 'Платеж не оплачен.'
        return Response({'message': message})
