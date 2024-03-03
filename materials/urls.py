from django.urls import path
from materials.apps import MaterialsConfig
from rest_framework.routers import DefaultRouter

from materials.views.course import CourseViewSet
from materials.views.lesson import LessonListAPIView, LessonCreateAPIView, LessonUpdateAPIView, LessonRetrieveAPIView, \
    LessonDeleteAPIView
from materials.views.subscription import UserSubscriptionAPIView

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('', LessonListAPIView.as_view(), name='lessons_list'),
    path('create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_detail'),
    path('<int:pk>/delete/', LessonDeleteAPIView.as_view(), name='lesson_delete'),
    # Subscription
    path('subs/', UserSubscriptionAPIView.as_view(), name='User_Subscription'),
] + router.urls
