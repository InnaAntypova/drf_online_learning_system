from rest_framework import serializers

from users.models import User, Payment
from users.serializers.payment import PaymentSerializer


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'avatar', 'phone', 'city']


class UserProfileSerializer(serializers.ModelSerializer):
    payments = serializers.SerializerMethodField()  # платежи пользователя

    def get_payments(self, instance):
        return PaymentSerializer(Payment.objects.filter(user=instance), many=True).data

    class Meta:
        model = User
        fields = ['email', 'avatar', 'phone', 'city', 'payments']


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password']
