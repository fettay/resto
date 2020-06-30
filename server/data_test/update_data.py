
import os
import sys
from getpass import getpass

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resto_server.settings')
django.setup()

from data.providers import PROVIDERS
from django.contrib.auth.models import User

DEFAULT_FETCH_FROM = 30
    

def get_user():
    email = input('Enter email for the user: ')
    password = getpass('Enter password for the user: ')
    user = User.objects.get(email=email, username=email)
    print("Successfully retrieved user")
    return user

def get_api(user):
    provider_name = input('Enter a provider (%s): ' % " | ".join(PROVIDERS.keys()))
    provider = PROVIDERS[provider_name]
    return provider.api(user)


def main():
    user = get_user()
    api = get_api(user)
    api.set_credentials()
    print("Successfully created credentials for %s" % user.email)
    api.login()
    api.update_data()
    print('We are done')


if __name__ == '__main__':
    main()
