1. Как развернуть проект:

    1. Клонируете проект в какую-либо директорию.
    2. Открываете терминал.
    3. Вводите команду cd sberbank_test_task/deploy.
    4. Вводите команду docker-compose build и ждете окончания выполнения.
    5. Вводите команду docker-compose up -d и ждете ее окончания (ждете когда Django в контейнере server1 запустится).
    6. Заходите в контейнер c сервером (он должен называться server-1)
    7. Открываете там терминал
    8. Вводите команду python3 manage.py migrate
    Вуаля вы развернули проект

2. Как наполнить БД данными:
    1. Вводите там команду python3 manage.py create_users_command
    У вас должно создаться три пользователя и у каждого свой токен

    username    Токен
    user1:      8116eec187d0be1588db0fa6f47ce73b75cbddb2,
    user2:      6a5c74da7b9ef80b8f0dbf151ee5bef68bae2310,
    user3:      5ae128abb337361a7be6b0e5aa415ce4535849c1

3. Как тестировать:
    !!!
    В КАЖДОМ вашем запросе вы должны добавить заголовок Authorization: Token <любой токен который указан выше>, токен
    выбираете в зависимости от того за какого пользователя вы хотите выполнять действия.
    !!!
    Тестировал через Postman
    1. API для фиксирования списка ссылок, которые посетил работник:
        - Метод: POST
        - URL: http://localhost:8000/visited_links
        - Пример тела запроса - {
                "links": [
                    "https://ya.ru/",
                    "https://ya.ru/search/?text=мемы+с+котиками",
                    "https://sber.ru",
                    "https://stackoverflow.com/questions/65724760/how-it-is",
                    "https://stackoverflow.com/questions/65724760/how-it-is/hello",
                    "https://stackoverflow.com/questions/65724760/how-it-is/helloworld",
                    "https://stackoverflow.com/questions/65724760/how-it-is/helloworldsomeworkd",
                    "https://stackoverflow.com/questions/65724760/how-it-is/helloworldsomeworkdd",
                    "https://stackoverflow.com/questions/65724760/how-it-is/helloworldsomeworkdddd",
                    "https://yandex.ru/"
                ]
            }
        - Если все хорошо:
            - Код ответа: 200
            - Тело ответа(Пример): {"status": "ok"}
        - Если ошибка на вашей стороне:
            - Код ответа: 400
            - Тело ответа (Пример): {"status": Описание ошибки}
        - Если ошибка на стороне сервера:
            - Код ответа: 500
            - Тело ответа: {"status": "Упс, что-то пошло не так!"}
    2. API для получения всех уникальных доменов, которые посещал работник:
        - Метод: GET
        - URL: http://localhost:8000/visited_domains
        - Кверистринги: 
            - from: Целочисленное положительное
            - to: Целочисленное положительное
        - Если все хорошо:
            - Код ответа: 200
            - Тело ответа(Пример): {
                    "domains": [
                        "ya.ru",
                        "sber.ru",
                        "stackoverflow.com",
                        "yandex.ru"
                    ],
                    "status": "ok"
                }
        - Если ошибка на вашей стороне:
            - Код ответа: 400
            - Тело ответа (Пример): {"status": Описание ошибки}
        - Если ошибка на стороне сервера:
            - Код ответа: 500
            - Тело ответа: {"status": "Упс, что-то пошло не так!"}


