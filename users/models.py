from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from education.models import NULLABLE


class UserRoles(models.TextChoices):
    """ Класс на создание ролей рользователя """

    MEMBER = 'member', _('member')
    MODERATOR = 'moderator', _('moderator')


class User(AbstractUser):
    """Модель для пользователей сервиса"""

    username = None

    email = models.EmailField(unique=True, verbose_name='почта')
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='страна', **NULLABLE)
    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.MEMBER)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
