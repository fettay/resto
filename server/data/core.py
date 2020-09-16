
from app.models import Order
from collections import namedtuple


class ProviderApi:
    def __init__(self, user, credentials=None):
        self._user = user
        self._credentials = credentials

    def set_credentials(self, email, setup_link):
        pass

    def login(self):
        pass

    def onboard(self):
        pass

    def update_data(self, start_from=None):
        raise NotImplementedError

    def live_orders(self):
        raise NotImplementedError


Provider = namedtuple('Provider', ['name', 'api'])


class LoginError(Exception):
    pass