from django.urls import path

from users.views.user_domains import UserDomainsViewSet

urlpatterns = [
    path(
        '',
        UserDomainsViewSet.as_view({
            'get': 'list',
        }),
        name='user_visited_domain'
    ),
]
