from django.core.management.base import BaseCommand

from users.seed.users_seed import create_users_seed


class Command(BaseCommand):
    """Команда для создания пользователей."""

    help = 'Создаем пользователей'

    def handle(self, *args, **options):
        """Создаем пользоватей."""
        create_users_seed()
        self.stdout.write(self.style.SUCCESS('Пользователи успешно созданы!'))
