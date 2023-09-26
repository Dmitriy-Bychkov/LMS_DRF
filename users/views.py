from rest_framework import viewsets

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ ViewSet - набор для основных CRUD - действий над пользователями """

    serializer_class = UserSerializer
    queryset = User.objects.all()
