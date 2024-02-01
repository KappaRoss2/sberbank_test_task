from django.db import models

from users.models.users import User


class WebResource(models.Model):
    """Модель веб-ресурса, который посещает пользователь."""

    url = models.URLField(
        verbose_name='Ссылка, которую посещал пользователь',
        unique=True,
    )


class Visit(models.Model):
    """M2M модель связывающая пользователя и посещенный им веб-ресурс."""

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='visited_user'
    )
    web_resource = models.ForeignKey(
        WebResource,
        verbose_name='Веб-ресурс',
        on_delete=models.CASCADE,
        related_name='visited_web_resource'
    )

    last_visit = models.DateTimeField(
        verbose_name='Дата визита',
    )
