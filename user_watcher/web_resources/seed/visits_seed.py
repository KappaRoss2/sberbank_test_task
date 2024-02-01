from django.utils.timezone import now

from users.models.users import User

from web_resources.models.resource import Visit
from web_resources.models.resource import WebResource


def create_visits_seed():
    """Создаем записи о посещении ресурсов пользователями."""
    current_time = now()
    user_ids = User.objects.all().values_list('id', flat=True)
    resource_ids = WebResource.objects.all().values_list('id', flat=True)
    visit_instances = []
    for user_id in user_ids:
        for resource_id in resource_ids:
            visit_instances.append(
                Visit(
                    user_id=user_id,
                    web_resource_id=resource_id,
                    last_visit=current_time
                )
            )
    Visit.objects.bulk_create(visit_instances)
