from rest_framework import serializers


class CreateResourceIncomingDataSerializer(serializers.Serializer):
    """Сериализатор для ссылок, которые посещал пользователь."""

    links = serializers.ListField(child=serializers.URLField(allow_blank=False, max_length=300), allow_empty=False)
