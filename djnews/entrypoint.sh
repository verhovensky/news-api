#! /bin/bash

apt-get update

if [ "$1" = "run_django" ]; then
  python manage.py makemigrations --no-input
  python manage.py migrate --no-input
  python manage.py collectstatic --no-input
  python manage.py test
  exec gunicorn parsernews.wsgi:application -b 0.0.0.0:8000 --reload
fi