from django.utils.timezone import now
from django.db import transaction

from config.consts import SUCCESS_STATUS

from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from web_resources.serializers.resource import CreateResourceIncomingDataSerializer
from web_resources.models.resource import WebResource
from web_resources.models.resource import Visit


class ResourceViewSet(ViewSet):
    """Вьюсет для ресурсов, которые посещает пользователь."""

    @transaction.atomic
    def create(self, request):
        """Метод в котором мы принимаем список ссылок посещенные пользователем и фиксируем их."""
        # NOTE: Не стал реализовывать создание/обновление записей через for, так как возможно размер списока
        # ссылок может достигать 1000 или даже больше.
        current_time = now()
        serialized_data = CreateResourceIncomingDataSerializer(data=request.data)
        serialized_data.is_valid(raise_exception=True)
        validated_data = serialized_data.validated_data
        urls = set(validated_data.get('links'))
        self._update_visit(urls, request.user.id, current_time)
        self._create_new_resources(urls)
        self._create_visits(urls, request.user.id, current_time)
        return Response(
            status=status.HTTP_200_OK,
            data={
                'status': SUCCESS_STATUS,
            }
        )

    def _update_visit(self, urls, user_id, current_time):
        """Обновляем время посещения тех ресурсов, которые пользователь посещал ранее и посетил снова.

        Args:
            urls (set): Множество ссылок.
            user_id (int): id пользователя.
            current_time (datetime): Время посещения ресурсов.
        """
        user_visit = Visit.objects.filter(user_id=user_id, web_resource__url__in=urls)
        updated_visit_instances = []
        for visit in user_visit:
            visit.last_visit = current_time
            updated_visit_instances.append(
                visit
            )
        Visit.objects.bulk_update(objs=updated_visit_instances, fields=['last_visit'])

    def _create_new_resources(self, urls):
        """Создаем записи о ресурсах в модель WebResource, которые еще не были зафиксированы в системе.

        Args:
            urls (set): Множество ссылок.
        """
        existing_web_resources = WebResource.objects.filter(url__in=urls).values_list('url', flat=True)
        new_urls = urls.difference(set(existing_web_resources))
        web_resource_instances = []
        for url in new_urls:
            web_resource_instances.append(
                WebResource(url=url)
            )
        WebResource.objects.bulk_create(web_resource_instances)

    def _create_visits(self, urls, user_id, current_time):
        """Создаем записи о ресурсах, которые пользователь посетил первый раз.

        Args:
            urls (set): Множество ссылок.
            user_id (int): id пользователя.
            current_time (datetime): Время посещения ресурсов.
        """
        visit_instances = []
        current_visited_resources = Visit.objects.filter(
            user_id=user_id,
            web_resource__url__in=urls
        ).values_list(
            'web_resource__url',
            flat=True,
        )
        new_visited_resources = urls.difference(set(current_visited_resources))
        new_resource_ids = WebResource.objects.filter(url__in=new_visited_resources).values_list('id', flat=True)
        for resource_id in new_resource_ids:
            visit_instances.append(
                Visit(
                    user_id=user_id,
                    web_resource_id=resource_id,
                    last_visit=current_time
                )
            )
        Visit.objects.bulk_create(visit_instances)
