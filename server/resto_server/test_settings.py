from resto_server.shared_settings import *
import os


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD", ""),
        'HOST': 'db',
        'PORT': '',
    }
}

BASE_URL = 'http://forecasteat.com:8000'
FUNCTION_APP_URL = 'http://localhost:7071'

# EMAIL SETTINGS

DEFAULT_FROM_EMAIL = 'ForecastEat <noreply@forecasteat.com>'
EMAIL_HOST = 'mail'
EMAIL_HOST_USER = '' 
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 25
EMAIL_USE_TLS = False
