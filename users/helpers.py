from django.contrib.auth.models import AnonymousUser

from users.models import UserRoles


def is_moderator(user):
    """ Проверяет является ли пользователь модератором """

    if isinstance(user, AnonymousUser):
        return False
    return user.role == UserRoles.MODERATOR
