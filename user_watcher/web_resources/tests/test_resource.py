from django.db.models import Count

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from config.consts import SUCCESS_STATUS

from users.models.users import User
from users.seed.users_seed import create_users_seed


class TestResourcesApi(APITestCase):
    """Класс для тестирования апи связанных с ресурсами."""

    @classmethod
    def setUpTestData(cls):
        create_users_seed()

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.get(username='user1')
        self.client.force_authenticate(user=self.user)

    def check_create_resources(self, payload):
        """Отправляем запрос и запускаем проверки.

        Args:
            payload (dict): Тело запроса
        """
        response = self.client.post(
            path='http://localhost:8000/visited_links',
            data=payload,
            format='json',
        )
        count_user_resources = User.objects.filter(
            id=self.user.id
        ).aggregate(
            Count('visited_user__web_resource')
        ).get('visited_user__web_resource__count')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('status'), SUCCESS_STATUS)
        self.assertEqual(len(payload['links']), count_user_resources)

    def test_create_resources(self):
        """Проверяем правильность создания ресурса."""
        payload = {
            'links': [
                'https://ya.ru/',
                'https://ya.ru/search/?text=мемы+с+котиками',
                'https://sber.ru',
                'https://stackoverflow.com/questions/65724760/how-it-is',
                'https://stackoverflow.com/questions/65724760/how-it-is/hello',
                'https://stackoverflow.com/questions/65724760/how-it-is/helloworld',
                'https://stackoverflow.com/questions/65724760/how-it-is/helloworldsomeworkd',
                'https://stackoverflow.com/questions/65724760/how-it-is/helloworldsomeworkdd',
                'https://stackoverflow.com/questions/65724760/how-it-is/helloworldsomeworkdddd',
                'https://yandex.ru/'
            ]
        }
        self.check_create_resources(payload)
        payload['links'].append('https://google.com/')
        self.check_create_resources(payload)

    def check_validate_resource_incoming_data(self, payload, expected_status_code, expected_resource_count):
        """Отправляем запрос и делаем проверки.

        Args:
            payload (dict): Тело запроса.
            expected_status_code (int): Ожидаемый код ответа.
            expected_resource_count (int): Ожидаемое количество записей.
        """
        response = self.client.post(
            path='http://localhost:8000/visited_links',
            data=payload,
            format='json',
        )
        count_user_resources = User.objects.filter(
            id=self.user.id
        ).aggregate(
            Count('visited_user__web_resource')
        ).get('visited_user__web_resource__count')
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(expected_resource_count, count_user_resources)

    def test_validate_incoming_data(self):
        """Проверяем правильность валидации данных."""
        incorrect_payload_key = {
            'linksssssss': [
                'https://ya.ru/',
                'https://ya.ru/search/?text=мемы+с+котиками',
                'https://sber.ru',
                'https://stackoverflow.com/questions/65724760/how-it-is',
                'https://stackoverflow.com/questions/65724760/how-it-is/hello',
                'https://stackoverflow.com/questions/65724760/how-it-is/helloworld',
                'https://stackoverflow.com/questions/65724760/how-it-is/helloworldsomeworkd',
                'https://stackoverflow.com/questions/65724760/how-it-is/helloworldsomeworkdd',
                'https://stackoverflow.com/questions/65724760/how-it-is/helloworldsomeworkdddd',
                'https://yandex.ru/'
            ]
        }

        self.check_validate_resource_incoming_data(incorrect_payload_key, status.HTTP_400_BAD_REQUEST, 0)

        incorrect_payload_resource = {
            'links': [
                'https://ya.ru/',
                'https://ya.ru/search/?text=мемы+с+котиками',
                'https://sber.ru',
                'https://stackoverflow.com/questions/65724760/how-it-is',
                'https://stackoverflow.com/questions/65724760/how-it-is/hello',
                'https://stackoverflow.com/questions/65724760/how-it-is/helloworld',
                'https://stackoverflow.c,,om/ques,tions/65724760/how-it-is/helloworldsomeworkd',
                'https://stackoverflow.com/questions/6572476,,,0/how-it-is/helloworldsomeworkdd',
                'https://stackoverflow.com/ques.ti.,ons/65724760/h.o.w.-.it-is/helloworldsomeworkdddd',
                'https://yandex.ru/'
            ]
        }

        self.check_validate_resource_incoming_data(incorrect_payload_resource, status.HTTP_400_BAD_REQUEST, 0)

        correct_payload = {
            'links': [
                'https://ya.ru/',
                'https://ya.ru/search/?text=мемы+с+котиками',
                'https://sber.ru',
                'https://stackoverflow.com/questions/65724760/how-it-is',
                'https://stackoverflow.com/questions/65724760/how-it-is/hello',
                'https://stackoverflow.com/questions/65724760/how-it-is/helloworld',
                'https://stackoverflow.com/questions/65724760/how-it-is/helloworldsomeworkd',
                'https://stackoverflow.com/questions/65724760/how-it-is/helloworldsomeworkdd',
                'https://stackoverflow.com/questions/65724760/how-it-is/helloworldsomeworkdddd',
                'https://yandex.ru/'
            ]
        }
        self.check_validate_resource_incoming_data(correct_payload, status.HTTP_200_OK, len(correct_payload['links']))
