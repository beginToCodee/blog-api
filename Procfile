web: waitress-serve --port=$PORT backend.wsgi:application
web: gunicorn backend.wsgi:application --log-file - --log-level debug
python manage.py collectstatic --noinput
manage.py migrate
