from django.utils.timezone import now

from users.models.users import User
from rest_framework.authtoken.models import Token


def create_users_seed():
    """Функция, которая создает пользователей."""
    user1 = User.objects.create(
        username='user1',
        first_name='Vadim',
        last_name='Grebnev',
        patronymic='Yurievich',
        email='someemail1@mail.ru',
    )
    user1.set_password('qwerty12345')
    user1.save()
    Token.objects.create(
        key='8116eec187d0be1588db0fa6f47ce73b75cbddb2',
        created=now(),
        user_id=user1.id
    )
    user2 = User.objects.create(
        username='user2',
        first_name='Milena',
        last_name='Serebrova',
        patronymic='Olegovna',
        email='someemail2@mail.ru',
    )
    user2.set_password('qwerty12345')
    user2.save()
    Token.objects.create(
        key='6a5c74da7b9ef80b8f0dbf151ee5bef68bae2310',
        created=now(),
        user_id=user2.id
    )
    user3 = User.objects.create(
        username='user3',
        first_name='Anton',
        last_name='Larionov',
        patronymic='Sergeevich',
        email='someemail3@mail.ru',
    )
    user3.set_password('qwerty12345')
    user3.save()
    Token.objects.create(
        key='5ae128abb337361a7be6b0e5aa415ce4535849c1',
        created=now(),
        user_id=user3.id
    )
