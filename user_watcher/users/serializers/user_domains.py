from django.utils import timezone

from django.db.models import Max
from django.db.models import Min
from django.utils.timezone import now

from rest_framework import serializers

from users.models.users import User


class UserDomainsIncomingDataSerializer(serializers.Serializer):
    """Сериализуем входящие данные для получения списка доменнов посещенных пользователем."""

    from_date = serializers.IntegerField(allow_null=False, required=False, min_value=0)
    to_date = serializers.IntegerField(allow_null=False, required=False, min_value=0)

    def validate(self, data):
        """Валидируем данные, чтобы получить данные сразу в формате дата-время.

        Returns:
            dict: валидные данные.
        """
        user_id = self.context.get('user_id')
        current_time = now()
        from_date = data.get('from_date')
        to_date = data.get('to_date')
        if not from_date:
            from_date = User.objects.filter(
                id=user_id
            ).aggregate(
                Min('visited_user__last_visit')
            ).get('visited_user__last_visit__min')
            from_date = from_date or current_time
        else:
            from_date = timezone.datetime.fromtimestamp(from_date)
        if not to_date:
            to_date = User.objects.filter(
                id=user_id
            ).aggregate(
                Max('visited_user__last_visit')
            ).get('visited_user__last_visit__max')
            to_date = to_date or current_time
        else:
            to_date = timezone.datetime.fromtimestamp(to_date)
        data['from_date'] = from_date
        data['to_date'] = to_date
        return data
