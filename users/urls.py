from django.urls import path
from users.apps import UsersConfig
from users.views.user import UserUpdateAPIView, UserProfileAPIView, UserRegistrationAPIView, UserListAPIView, \
    DestroyAPIView
from users.views.payment import PaymentListAPIView

app_name = UsersConfig.name

urlpatterns = [
    # user
    path('registr/', UserRegistrationAPIView.as_view(), name='user_registration'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='user_profile_update'),
    path('all/', UserListAPIView.as_view(), name='all_users'),
    path('delete/<int:pk>/', DestroyAPIView.as_view(), name='delete_user'),
    path('<int:pk>/profile/', UserProfileAPIView.as_view(), name='user_profile'),
    # payment
    path('payments/', PaymentListAPIView.as_view(), name='payments_list')
]
