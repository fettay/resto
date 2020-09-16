from data.core import ProviderApi, LoginError, Provider
from app.models import Order, Credentials, Meal, Restaurant, Review, User

import pandas as pd
from retry import retry
import requests
from django.utils.crypto import get_random_string

import json
import logging
from urllib.parse import quote
from collections import namedtuple


LOGIN_URL = "https://restaurant-hub.deliveroo.net/api/session"
RESTO_URL = "https://restaurant-hub.deliveroo.net/api/restaurants/{restaurant_id}"
REGISTER_URL = "https://restaurant-hub.deliveroo.net/api/reset-password"
ORDERS_URL = RESTO_URL + "/orders?date={date}&end_date={date}&starting_after={start_after}&sort_date={sort_date}&with_summary=no"
ITEMS_URL = "https://restaurant-hub.deliveroo.net/api/orders/{order_id}"
REVIEWS_URL = RESTO_URL + "/reviews?stars=&sort_date={sort_date}&starting_after={start_after}"
TIMEZONE = "Europe/Paris"
PROVIDER_NAME = 'Deliveroo'


MySqlInput = namedtuple('MySqlInput', ['model', 'data'])


@retry(ValueError, tries=5, delay=2)
def _get_order_meal_single(args):
    token, order_id = args
    response = requests.get(ITEMS_URL.format(order_id=order_id), headers={'authorization': token})
    if response.status_code != 200:
        raise ValueError
    items = response.json()['items']
    all_meals = []
    for item in items:
        all_meals.append((item['name'], item['quantity'], item['category_name']))
        for modifier in item.get('modifiers', []):
            all_meals.append((modifier['name'], item['quantity'], 'Modifiers'))
    return all_meals


class DeliverooApi(ProviderApi):

    def __init__(self, user, credentials=None):
        self._token = None
        self.restaurants = None
        super().__init__(user, credentials)

    @retry(ValueError, tries=5, delay=2)
    def _request(self, url):
        response = requests.get(url, headers={'authorization': self._token})
        if response.status_code != 200:
            raise ValueError
        return response

    def _get_credentials(self):
        if self._credentials is not None:
            return json.loads(self._credentials)
        
        self._credentials = Credentials.objects.get(owner=self._user, provider=PROVIDER_NAME).credentials
        return json.loads(self._credentials)

    @staticmethod
    def _login_api(email, password):
        res = requests.post(LOGIN_URL, json={'email': email, 'password': password})
        if res.status_code != 200:
            raise LoginError('Wrong credentials')
        return res.json()

    @staticmethod
    def _register(token, password):
        res = requests.post(REGISTER_URL, json={'password': password,
                                                'password_confirmation': password,
                                                'reset_token': token})
        if res.status_code != 200:
            raise LoginError('Wrong link')
        return res.json()

    def set_credentials(self, email, setup_link):
        try:
            Credentials.objects.get(owner=self._user, provider=PROVIDER_NAME)
            logging.info("Already found credentials for the user")
            return
        except Credentials.DoesNotExist:
            pass
    
        token = setup_link.split('/')[-1]
        password = get_random_string()
        _ = self._register(token, password)
        credentials = Credentials(owner=self._user, provider=PROVIDER_NAME,
                                  credentials=json.dumps({'email': email, 'password': password}))
        return credentials

    def login(self):
        cred = self._get_credentials()
        res = self._login_api(cred["email"], cred["password"])
        self.restaurants = [resto for company in res['restaurant_companies'] for resto in company['restaurants']]
        self._token = "Bearer " + res['access_token']
        self._update_resto_list()
        return res

    def _update_resto_list(self):
        formatted_data = [self._format_restaurant(resto) for resto in self.restaurants]
        my_sql_input = MySqlInput(Restaurant, formatted_data)
        self.insert_to_mysql([my_sql_input])

    def _format_order(self, order, restaurant):
        order_dict = {'order_number': order['order_number'], 
                      'order_id': order['order_id'], 
                      'status': order['status'], 
                      'amount': float(order['amount']['formatted'][1:]), 
                      'date': pd.Timestamp(order['timeline']['placed_at']).to_pydatetime(),
                      'provider': PROVIDER_NAME,
                      'restaurant': restaurant,
                      'owner': self._user}
        
        return Order(**order_dict)

    def _format_restaurant(self, restaurant):
        resto_dict = {'resto_id': restaurant['id'], 
                      'owner': self._user, 
                      'name': restaurant['name'], 
                      'latitude': restaurant['location']['lat'], 
                      'longitude': restaurant['location']['lng'],
                      'provider': PROVIDER_NAME}
        
        return Restaurant(**resto_dict)

    def _format_meal(self, meal, order):
        meal_dict = {'category': meal[2].lower(),
                     'title': meal[0].lower(), 
                     'provider': PROVIDER_NAME,
                     'owner': self._user,
                     'quantity': meal[1]}

        meal_object = Meal(**meal_dict)
        meal_object.order_id = order.order_id
        return meal_object

    def _format_review(self, review, restaurant):

        review_dict = {'owner': self._user, 
                       'restaurant': restaurant,
                       'provider': PROVIDER_NAME,
                       'date': pd.Timestamp(review['created_at']).to_pydatetime(),
                       'comment': review['rating_comment'],
                       'rating': review['rating_stars']}
        
        review_object = Review(**review_dict)
        review_object.order_id = review['order_uuid']
        return review_object

    def _get_reviews_by_resto(self, resto, date):
        last_fetched_id = None
        all_reviews = []

        if date.tz is None:
            date = date.tz_localize('UTC')

        date_str = (date + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
        while True:
            if last_fetched_id is None:
                url = REVIEWS_URL.format(restaurant_id=resto.resto_id, start_after="0", sort_date=date_str)
            else:
                url = REVIEWS_URL.format(restaurant_id=resto.resto_id, start_after=last_fetched_id, sort_date=date_str)

            reviews = self._request(url).json()
            new_reviews = [self._format_review(r, resto) for r in reviews['reviews']]
            new_reviews = [r for r in new_reviews if r is not None and r.date >= date]

            if len(new_reviews) == 0 or (last_fetched_id is not None and new_reviews[-1].order_id == new_reviews[-1].order_id):
                break 

            all_reviews.extend(new_reviews)
            last_fetched_id = all_reviews[-1].order_id
    
        return all_reviews

    def _get_orders_by_resto(self, resto, date, last_order):
        if last_order is None:
            last_timestamp = None
            last_fetched_id = None
        else:
            last_timestamp = pd.Timestamp.now(tz=TIMEZONE)
            last_fetched_id = last_order.order_id
        all_orders = []
        while True:
            date_str = date.strftime("%Y-%m-%d")
            if last_fetched_id is None:
                url = ORDERS_URL.format(restaurant_id=resto.resto_id, start_after="",
                                            date=date_str, sort_date="")
            else:
                timestamp_str = quote(str(last_timestamp).replace(" ", "T").replace("+", " "))
                url = ORDERS_URL.format(restaurant_id=resto.resto_id, start_after=last_fetched_id,
                                            date=date_str, sort_date=timestamp_str)

            orders = self._request(url).json()
            new_orders = [self._format_order(o, resto) for o in orders['orders']]

            if len(new_orders) == 0 or (last_timestamp is not None and len(all_orders) > 0 and new_orders[-1].order_id == all_orders[-1].order_id):
                break 

            all_orders.extend(new_orders)
            last_fetched_id = all_orders[-1].order_id
            last_timestamp = all_orders[-1].date
        return all_orders

    def _get_meals_by_resto(self, orders):
        args = [(self._token, order.order_id) for order in orders]

        all_items = map(_get_order_meal_single, args)
        
        meals = [self._format_meal(item, order) for items, order in zip(all_items, orders) for item in items]
        return meals

    def _fetch_restaurant_data(self, resto, date, last_order=None):
        all_orders = self._get_orders_by_resto(resto, date, last_order)
        all_meals = self._get_meals_by_resto(all_orders)
        all_reviews = self._get_reviews_by_resto(resto, date)
        logging.info('Found {orders} orders, {meals} meals, {reviews} reviews for user {user} on {date} and resto {resto}'
                     .format(orders=len(all_orders), meals=len(all_meals), reviews=len(all_reviews), user=self._user.id,
                             date=str(date), resto=resto.resto_id))
        return all_orders, all_meals, all_reviews

    def onboard(self, ndays):
        logging.info("Onboarding user %s" % self._user.id)
        user_info = self.login()
        splitted_name = user_info['name'].split(' ')
        self._user.first_name = splitted_name[0]

        if len(splitted_name) > 1:
            self._user.last_name = " ".join(splitted_name[1:])

        logging.info("Retrieved personal info for user %s" % self._user.id)
        self._user.save()
        today = pd.Timestamp.today().floor("1d")
        logging.info("Retrieving data for user %s for %d days" % (self._user.id, ndays))
        for i in range(ndays, -1, -1):
            date = today - pd.Timedelta(days=i)
            my_sql_data = self.get_data_per_date(date)
            self.insert_to_mysql(my_sql_data)
        
        logging.info("Finished onboarding for user %s" % self._user.id)
    
    def update_data(self):
        last_order = self._get_last_fetched()
        today = pd.Timestamp.today().floor("1d")
        last_fetched_date = pd.Timestamp(last_order.date).tz_localize(None)
        number_of_days = (today - last_fetched_date).days

        # Days starting from scatch
        for i in range(number_of_days + 1):
            date = last_fetched_date + pd.Timedelta(days=i)
            my_sql_data = self.get_data_per_date(date)
            self.insert_to_mysql(my_sql_data)
        
        # Last day only update
        self.get_last_data(last_order)

    def get_last_data(self, last_order):
        all_orders = []
        all_meals = []
        all_reviews = []
        for resto in self.restaurants:
            resto = Restaurant.objects.get(resto_id=resto['id'], owner=self._user, provider=PROVIDER_NAME)
            resto_orders, resto_meals, resto_reviews = self._fetch_restaurant_data(resto, pd.Timestamp(last_order.date), last_order=last_order)
            all_meals.extend(resto_meals)
            all_orders.extend(resto_orders)
            all_reviews.extend(resto_reviews)
        return [MySqlInput(Order, all_orders), MySqlInput(Meal, all_meals), MySqlInput(Review, all_reviews)]
            
    def get_data_per_date(self, date=None):
        all_orders = []
        all_meals = []
        all_reviews = []
        for resto in self.restaurants:
            resto = Restaurant.objects.get(resto_id=resto['id'], owner=self._user, provider=PROVIDER_NAME)
            resto_orders, resto_meals, resto_reviews = self._fetch_restaurant_data(resto, date)
            all_meals.extend(resto_meals)
            all_orders.extend(resto_orders)
            all_reviews.extend(resto_reviews)
        return [MySqlInput(Order, all_orders), MySqlInput(Meal, all_meals), MySqlInput(Review, all_reviews)]

    def insert_to_mysql(self, my_sql_input):
        for inp in my_sql_input:
            inp.model.objects.bulk_create(inp.data, ignore_conflicts=True)
        
    def _get_last_fetched(self):
        last_order = Order.objects.filter(owner=self._user).latest('date')
        return last_order


DELIVEROO = Provider(PROVIDER_NAME, DeliverooApi)
