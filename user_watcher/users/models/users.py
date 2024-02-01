from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""

    patronymic = models.CharField(verbose_name='Отчество', null=True)
