import os
from carsapi.settings.base import *


SECRET_KEY = 'django-insercure-key'

ALLOWED_HOSTS = ["*"]

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}