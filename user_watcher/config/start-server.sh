wait-for-it primarydb:5432 --timeout=60
python manage.py migrate
python manage.py runserver 0.0.0.0:8000