from resto_server.shared_settings import *


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'db',
        'PORT': '',
    }
}

BASE_URL = 'http://localhost:8000'
FUNCTION_APP_URL = 'http://localhost:7071'

# EMAIL SETTINGS

DEFAULT_FROM_EMAIL = 'ForecastEat <noreply@forecasteat.com>'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'forecasteat@gmail.com' 
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
