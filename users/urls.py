from django.urls import path
from users.apps import UsersConfig
from users.views.user import UserUpdateAPIView, UserProfileAPIView
from users.views.payment import PaymentListAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('<int:pk>/update/', UserUpdateAPIView.as_view(), name='user_profile_update'),
    path('<int:pk>/profile/', UserProfileAPIView.as_view(), name='user_profile'),

    path('payments/', PaymentListAPIView.as_view(), name='payments_list')
]
