from celery import shared_task
import logging
from django.conf import settings
from django.contrib.auth.models import User

from data.providers import PROVIDERS


@shared_task
def onboard_user(user_id: int, provider: str):
    logging.info('Python HTTP trigger function processed a request.')
    user = User.objects.get(pk=user_id)
    api = PROVIDERS[provider.lower()].api(user)
    
    logging.info("Successfuly retrieved the user and credentials starts loading data")
    # api.onboard(settings.APP["DEFAULT_FETCH_FROM"])
    api.onboard(5)
    logging.info("Data is fetched sending reset password form to the user")
    requests.post(settings.BASE_URL + "/reset_password", {'email': user.email})
    logging.info("Done processing")
