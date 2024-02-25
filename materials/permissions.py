from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """ Класс для проверки принадлежности к Модератору """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='MODERATOR').exists()


class IsOwner(BasePermission):
    """ Класс для проверки принадлежности к владельцу объекта """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner
