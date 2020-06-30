from resto_server.shared_settings import *


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

BASE_URL = 'http://localhost:8000'

# EMAIL SETTINGS

DEFAULT_FROM_EMAIL = 'ForecastEat <noreply@forecasteat.com>'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'forecasteat@gmail.com' 
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_PORT = 587
EMAIL_USE_TLS = True