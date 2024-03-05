from django.contrib.auth.models import Group, Permission
from rest_framework.test import force_authenticate, APIClient, APITestCase
from rest_framework import status
from rest_framework.utils import json

from materials.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):
    """ Тестирование CRUD по Lesson (Урок) """

    def setUp(self) -> None:
        # группа для пользователя
        member_group, created = Group.objects.get_or_create(name='MEMBER')
        if created:
            permissions = Permission.objects.filter(
                codename__in=['add_course', 'change_course', 'delete_course', 'view_course', 'add_lesson',
                              'change_lesson', 'delete_lesson', 'view_lesson']
            )
            member_group.permissions.set(permissions)

        moderator_group, created = Group.objects.get_or_create(name='MODERATOR')
        if created:
            permissions = Permission.objects.filter(
                codename__in=['change_course', 'view_course', 'change_lesson', 'view_lesson']
            )
            moderator_group.permissions.set(permissions)

        # пользователь для теста
        self.user = User.objects.create(
            email='test1@test.ru', is_active=True
        )
        self.user.groups.add(member_group)
        # модератор для теста
        self.moder = User.objects.create(
            email='moder_test@test.ru', is_active=True, is_staff=True
        )
        self.moder.groups.add(moderator_group)

        # курс для теста
        self.course = Course.objects.create(
            title='test',
            description='test',
            owner=self.user
        )
        # урок для теста
        self.lesson = Lesson.objects.create(
            title='test',
            description='test',
            course=self.course,
            owner=self.user
        )

    def test_create_lesson(self):
        """ Тест на создание урока """
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'test1',
            'description': 'test1',
            'course': self.course.id,
            'owner': self.user.id
        }
        response = self.client.post('/create/', data=data)
        # print(response.data)
        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEquals(
            response.json(),
            {'id': 2, 'title': 'test1', 'description': 'test1', 'image': None, 'video_url': None,
             'course': self.course.id, 'owner': self.user.id}
        )
        # проверка модератора
        self.client.force_authenticate(user=self.moder)
        data = {
            'title': 'test2',
            'description': 'test2',
            'course': self.course.id,
            'owner': self.user.id
        }
        response = self.client.post('/create/', data=data)
        self.assertEquals(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_get_list_lessons(self):
        """ Тест на получение всех уроков """
        self.client.force_authenticate(user=self.user)
        response = self.client.get('')
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEquals(
            Lesson.objects.all().count(), 1
        )

    def test_detail_lesson(self):
        """ Тест на получение детализации по уроку """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/{self.lesson.id}/')
        # print(response.data)
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEquals(
            response.json(),
            {'id': self.lesson.id, 'title': 'test', 'description': 'test', 'image': None, 'video_url': None,
             'course': self.course.id,
             'owner': self.user.id}
        )

    def test_update_lesson(self):
        """ Тест для обновления урока """
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'test1_update',
            'description': 'test1_update',
            'course': self.course.pk,
            'owner': self.user.pk
        }
        response = self.client.patch(f'/{self.lesson.id}/update/', data=data)
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEquals(
            response.json(),
            {'id': self.lesson.id, 'title': 'test1_update', 'description': 'test1_update', 'image': None,
             'video_url': None,
             'course': self.course.id, 'owner': self.user.id}
        )
        # проверка модератора
        self.client.force_authenticate(user=self.moder)
        data = {
            'title': 'test1_update_moder',
            'description': 'test1_update_moder',
            'course': self.course.pk,
            'owner': self.user.pk
        }
        response = self.client.patch(f'/{self.lesson.id}/update/', data=data)
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEquals(
            response.json(),
            {'id': self.lesson.id, 'title': 'test1_update_moder', 'description': 'test1_update_moder', 'image': None,
             'video_url': None, 'course': self.course.id, 'owner': self.user.id}
        )

    def test_delete_lesson(self):
        """ Тест для удаления урока """
        # проверка модератора
        self.client.force_authenticate(user=self.moder)
        response = self.client.delete(f'/{self.lesson.id}/delete/')
        self.assertEquals(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
        # проверка пользователя
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/{self.lesson.id}/delete/')
        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEquals(
            Lesson.objects.all().count(), 0
        )


class UserSubscriptionTestCase(APITestCase):
    """ Тестирование UserSubscription (Подписки на курс у пользователя) """

    def setUp(self) -> None:
        # пользователь для теста
        self.user = User.objects.create(
            email='test1@test.ru', is_active=True
        )
        # курс для теста
        self.course = Course.objects.create(
            title='test',
            description='test',
            owner=self.user
        )

    def test_subscription(self):
        """ Тестирование добавления/удаления подписки """
        self.client.force_authenticate(user=self.user)
        data = {
            'user': self.user.id,
            'course': self.course.id
        }
        # добавление подписки
        response = self.client.post('/subs/', data=data)
        # print(response.data)
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEquals(
            response.json(),
            {'message': 'Подписка добавлена'}
        )
        # удаление подписки
        response = self.client.post('/subs/', data=data)
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEquals(
            response.json(),
            {'message': 'Подписка удалена'}
        )
