from rest_framework import viewsets, permissions

from users.models import User
from users.permissions import IsOwnerOrReadOnly
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ ViewSet - набор для основных CRUD - действий над пользователями """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        """ Позволяем создавать и редактировать только свой профиль """

        serializer.save(owner=self.request.user)
