from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from config.consts import SUCCESS_STATUS

from users.models.users import User
from users.seed.users_seed import create_users_seed

from web_resources.seed.resources_seed import create_resources_seed
from web_resources.seed.visits_seed import create_visits_seed


class TestVisitApi(APITestCase):
    """Тестируем апи связанные с визитами на какие-либо ресурсы пользователем."""

    @classmethod
    def setUpTestData(cls):
        create_users_seed()
        create_resources_seed()
        create_visits_seed()

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.get(username='user1')
        self.client.force_authenticate(user=self.user)

    def check_get_domains(self, expected_domains, expected_status_code, query_params=None):
        """Отправляем запрос и запускаем проверки для получения уникальных доменов.

        Args:
            expected_domains (list): Список ожидаемых уникальных доменов.
            expected_status_code (int): Ожидаемый код ответа.
            query_params (dict, optional): Кверипараметры. Defaults to None.
        """
        response = self.client.get(
            path='http://localhost:8000/visited_domains',
            data=query_params
        )
        expected_domains.sort()
        response_domains = response.json().get('domains')
        response_domains.sort()
        response_status = response.json().get('status')
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response_domains, expected_domains)
        self.assertEqual(response_status, SUCCESS_STATUS)

    def check_validate_incoming_data_for_get_domain(self, expected_status_code, query_params=None):
        """Отправляем запрос и запускаем проверки для валидирования данных.

        Args:
            expected_status_code (int): Ожидаемый код ответа.
            query_params (dict, optional): Кверипараметры. Defaults to None.
        """
        response = self.client.get(
            path='http://localhost:8000/visited_domains',
            data=query_params
        )
        self.assertEqual(response.status_code, expected_status_code)

    def test_get_domains(self):
        """Тестируем получение уникальных доменнов."""
        correct_domains = ['sber.ru', 'stackoverflow.com', 'ya.ru', 'yandex.ru']
        self.check_get_domains(correct_domains, status.HTTP_200_OK)
        query_params = {
            'from': 1545221231,
            'to': 54654654645
        }
        self.check_get_domains(correct_domains, status.HTTP_200_OK, query_params)
        query_params = {
            'to': '54654654645'
        }
        self.check_get_domains(correct_domains, status.HTTP_200_OK, query_params)
        query_params = {
            'from': 1545221231,
        }
        self.check_get_domains(correct_domains, status.HTTP_200_OK, query_params)

    def test_validate_incoming_data_for_get_domain(self):
        """Тестируем валидацию входных данных."""
        query_params = {
            'from': 1545221231,
            'to': -54654654645
        }
        self.check_validate_incoming_data_for_get_domain(status.HTTP_400_BAD_REQUEST, query_params)
        query_params = {
            'from': -1545221231,
            'to': 54654654645
        }
        self.check_validate_incoming_data_for_get_domain(status.HTTP_400_BAD_REQUEST, query_params)
        query_params = {
            'from': 1545221231,
            'to': 54654654645
        }
        self.check_validate_incoming_data_for_get_domain(status.HTTP_200_OK, query_params)
