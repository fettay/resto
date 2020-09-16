import logging
import requests

from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User

from app.models import Credentials
from data.providers import PROVIDERS


@shared_task
def onboard_user(user_id: int, provider: str, credentials: Credentials):
    logging.info('Python HTTP trigger function processed a request.')
    # user = User.objects.get(pk=user_id)
    # api = PROVIDERS[provider.lower()].api(user, credentials)
    
    user = User.objects.get(pk=2)

    logging.info("Successfuly retrieved the user and credentials starts loading data")
    logging.info('Userid: %d' % user.id)
    logging.info('Provider: %s' % provider)
    # api.onboard(settings.APP["DEFAULT_FETCH_FROM"])
    # api.onboard(5)
    logging.info("Data is fetched sending reset password form to the user")
    requests.post(settings.WEB_CONTAINER_URL + "/reset_password", {'email': user.email})
    logging.info("Done processing")
