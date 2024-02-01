from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from config.consts import SUCCESS_STATUS
from users.serializers.user_domains import UserDomainsIncomingDataSerializer
from web_resources.models.resource import Visit

from tldextract import extract


class UserDomainsViewSet(ViewSet):

    def list(self, request):
        """Получаем список доменнов, которые посещал пользователь."""
        query_params = {}
        if from_date := request.query_params.get('from'):
            query_params['from_date'] = from_date
        if to_date := request.query_params.get('to'):
            query_params['to_date'] = to_date
        serialized_data = UserDomainsIncomingDataSerializer(
            data=query_params,
            context={'user_id': request.user.id}
        )
        serialized_data.is_valid(raise_exception=True)
        validated_data = serialized_data.validated_data
        from_date, to_date = validated_data.get('from_date'), validated_data.get('to_date')
        resources = Visit.objects.filter(
            user_id=request.user.id,
            last_visit__range=(from_date, to_date)
        ).values_list(
            'web_resource__url', flat=True
        )
        domains = set()
        for resource in resources:
            domain = extract(resource).registered_domain
            domains.add(domain)

        result = {
            'domains': domains,
            'status': SUCCESS_STATUS,
        }
        return Response(
            status=status.HTTP_200_OK,
            data=result
        )
