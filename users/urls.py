from django.urls import path
from users.apps import UsersConfig
from users.views.user import UserUpdateAPIView, UserProfileAPIView, UserRegistrationAPIView, UserListAPIView, \
    DestroyAPIView
from users.views.payment import PaymentListAPIView, PaymentCreateAPIView, PaymentStatusAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = UsersConfig.name

urlpatterns = [
    # user
    path('registr/', UserRegistrationAPIView.as_view(), name='user_registration'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='user_profile_update'),
    path('all/', UserListAPIView.as_view(), name='all_users'),
    path('delete/<int:pk>/', DestroyAPIView.as_view(), name='delete_user'),
    path('<int:pk>/profile/', UserProfileAPIView.as_view(), name='user_profile'),
    # JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # payment
    path('payments/', PaymentListAPIView.as_view(), name='payments_list'),
    path('create_payment/', PaymentCreateAPIView.as_view(), name='create_payment'),
    path('status/<int:pk>/', PaymentStatusAPIView.as_view(), name='payment_status')
]
