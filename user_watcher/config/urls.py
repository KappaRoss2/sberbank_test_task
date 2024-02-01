from django.contrib import admin
from django.urls import path
from django.urls import include
from rest_framework.authtoken.views import obtain_auth_token

api_urls = [
    path('token-auth/', obtain_auth_token, name='api_token_auth'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
    path('visited_links', include('web_resources.urls.resource')),
    path('visited_domains', include('users.urls.visited_domains')),
]
