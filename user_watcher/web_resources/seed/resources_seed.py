from web_resources.models.resource import WebResource


def create_resources_seed():
    """Создаем записи о ресурсах."""
    resources = [
        'https://ya.ru/',
        'https://ya.ru/search/?text=мемы+с+котиками',
        'https://sber.ru',
        'https://stackoverflow.com/questions/65724760/how-it-is',
        'https://stackoverflow.com/questions/65724760/how-it-is/hello',
        'https://stackoverflow.com/questions/65724760/how-it-is/helloworld',
        'https://stackoverflow.com/questions/65724760/how-it-is/helloworldsomeworkd',
        'https://stackoverflow.com/questions/65724760/how-it-is/helloworldsomeworkdd',
        'https://stackoverflow.com/questions/65724760/how-it-is/helloworldsomeworkdddd',
        'https://yandex.ru/'
    ]
    resource_instance = []
    for resource in resources:
        resource_instance.append(WebResource(url=resource))

    WebResource.objects.bulk_create(resource_instance)
