from django.urls import path

from web_resources.views.resource import ResourceViewSet

urlpatterns = [
    path(
        '',
        ResourceViewSet.as_view({
            'post': 'create',
        }),
        name='user_visits'
    ),
]
