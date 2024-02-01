import json

from rest_framework import status


class ErrorInspectorMiddleware:
    """Возвращаем ошибки одном формате."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if (response.status_code >= status.HTTP_400_BAD_REQUEST
                and response.status_code < status.HTTP_500_INTERNAL_SERVER_ERROR):
            error_data = {
                'status': json.loads(response.content)
            }
            response.content = json.dumps(error_data, ensure_ascii=False)
        elif (response.status_code >= status.HTTP_500_INTERNAL_SERVER_ERROR
              and response.status_code <= status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED):
            error_data = {
                'status': 'Упс, что-то пошло не так!'
            }
            response.content = json.dumps(error_data, ensure_ascii=False)
        return response
