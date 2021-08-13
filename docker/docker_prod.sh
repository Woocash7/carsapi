#!/bin/sh
python manage.py migrate --noinput --settings=carsapi.settings.prod &&
python manage.py loaddata test_fixtures.yaml --settings=carsapi.settings.prod &&
python manage.py collectstatic --noinput --settings=carsapi.settings.prod  &&
gunicorn carsapi.wsgi:application --bind 0.0.0.0:8000 --workers 3