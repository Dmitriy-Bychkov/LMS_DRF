from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение - только владелец может редактировать профиль
    """

    def has_object_permission(self, request, view, obj):
        # Разрешены все GET-запросы и запросы на создание нового профиля
        if request.method in permissions.SAFE_METHODS or request.method == 'POST':
            return True
        # Разрешено редактирование только владельцу профиля
        if obj != request.user:
            raise PermissionDenied("Вы не можете редактировать чужого пользователя!")
        return obj == request.user
