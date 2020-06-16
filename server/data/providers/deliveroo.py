from data.core import ProviderApi, LoginError, Provider
from app.models import Order, Credentials, Meal, Restaurant, Review

from tqdm import tqdm
import pandas as pd
from retry import retry
import requests

import json
import pprint
from datetime import datetime
from urllib.parse import quote
from getpass import getpass
from collections import namedtuple


LOGIN_URL = "https://restaurant-hub.deliveroo.net/api/session"
RESTO_URL = "https://restaurant-hub.deliveroo.net/api/restaurants/{restaurant_id}"
ORDERS_URL = RESTO_URL + "/orders?date={date}&end_date={date}&starting_after={start_after}&sort_date={sort_date}&with_summary=no"
ITEMS_URL = RESTO_URL + "/order_items?start_date={date}&end_date={date}&group_modifiers=true"
REVIEWS_URL = RESTO_URL + "/reviews?stars=&sort_date={sort_date}&starting_after={start_after}"
TIMEZONE = "Europe/Paris"
PROVIDER_NAME = 'Deliveroo'


MySqlInput = namedtuple('MySqlInput', ['model', 'data'])


class DeliverooApi(ProviderApi):

    def __init__(self, user):
        self._token = None
        self.restaurants = None
        self._mysqlcursor = None 
        super().__init__(user)

    @retry(ValueError, tries=5, delay=2)
    def _request(self, url):
        response = requests.get(url, headers={'authorization': self._token})
        if response.status_code != 200:
            print('hello')
            raise ValueError
        return response

    def _get_credentials(self):
        cred = Credentials.objects.get(owner_id=self._user, provider=PROVIDER_NAME).credentials
        return json.loads(cred)

    @staticmethod
    def _login_api(email, password):
        res = requests.post(LOGIN_URL, json={'email': email, 'password': password})
        if res.status_code != 200:
            raise LoginError('Wrong credentials')
        return res.json()

    def set_credentials(self):
        try:
            Credentials.objects.get(owner_id=self._user, provider=PROVIDER_NAME)
            print("Already found credentials for the user")
            return
        except Credentials.DoesNotExist:
            pass
        while True:
            email = input("Enter your deliveroo-hub username: ")
            password = getpass("Enter your deliveroo-hub password: ")
            try:
                login = self._login_api(email, password)
                break
            except LoginError:
                print("Invalid credentials retrying")
        credentials = Credentials(owner_id=self._user, provider=PROVIDER_NAME,
                                  credentials=json.dumps({'email': email, 'password': password}))
        credentials.save()

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
                      'owner_id': self._user}
        
        return Order(**order_dict)

    def _format_restaurant(self, restaurant):
        resto_dict = {'resto_id': restaurant['id'], 
                      'owner_id': self._user, 
                      'name': restaurant['name'], 
                      'latitude': restaurant['location']['lat'], 
                      'longitude': restaurant['location']['lng'],
                      'provider': PROVIDER_NAME}
        
        return Restaurant(**resto_dict)

    def _format_meal(self, order, restaurant, date):
        meal_dict = {'category': order['category_name'].lower(),
                      'title': order['name'].lower(), 
                      'date': pd.Timestamp(date, tz=TIMEZONE).floor("1d").to_pydatetime(),
                      'provider': PROVIDER_NAME,
                      'restaurant': restaurant,
                      'owner_id': self._user,
                      'quantity': order['quantity']}
        
        return Meal(**meal_dict)


    def _format_review(self, review, restaurant):

        review_dict = {'owner_id': self._user, 
                      'restaurant': restaurant,
                      'provider': PROVIDER_NAME,
                      'date': pd.Timestamp(review['created_at']).to_pydatetime(),
                      'comment': review['rating_comment'],
                      'rating': review['rating_stars']}
        
        review_object = Review(**review_dict)
        review_object.order_id_id = review['order_uuid']
        return review_object


    def _get_reviews_by_resto(self, resto, date):
        last_fetched_id = None
        all_reviews = []
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

            if len(new_reviews) == 0 or (last_fetched_id is not None and new_reviews[-1].order_id_id == new_reviews[-1].order_id_id):
                break 

            all_reviews.extend(new_reviews)
            last_fetched_id = all_reviews[-1].order_id_id
    
        return all_reviews


    def _get_orders_by_resto(self, resto, date):
        last_timestamp = None
        last_fetched_id = None
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

            if len(new_orders) == 0 or (last_timestamp is not None and new_orders[-1].order_id == all_orders[-1].order_id):
                break 

            all_orders.extend(new_orders)
            last_fetched_id = all_orders[-1].order_id
            last_timestamp = all_orders[-1].date
        return all_orders

    def _get_meals_by_resto(self, resto, date):
        items_sold_url = ITEMS_URL.format(restaurant_id=resto.resto_id, date=date.strftime('%Y-%m-%d'))
        meals = self._request(items_sold_url).json()
        meals = [self._format_meal(m, resto, date) for m in meals]
        return meals

    def _fetch_restaurant_data(self, resto, date):
        all_orders = self._get_orders_by_resto(resto, date)
        all_meals = self._get_meals_by_resto(resto, date)
        all_reviews = self._get_reviews_by_resto(resto, date)
        return all_orders, all_meals, all_reviews

    def onboard(self, ndays):
        user_info = self.login()
        splitted_name = user_info['name'].split(' ')
        self._user.first_name = splitted_name[0]

        if len(splitted_name) > 1:
            self._user.last_name = " ".join(splitted_name[1:])
    
        self._user.save()
        today = pd.Timestamp.today().floor("1d")
        print('Hey %s, we are loading your data' % (self._user.first_name))
        for i in tqdm(range(ndays + 1, 0, -1), total=ndays):
            date = today - pd.Timedelta(days=i)
            my_sql_data = self.get_data_per_date(date)
            self.insert_to_mysql(my_sql_data)
    
    def update_data(self):
        last_fetched_date = self._get_last_fetched()
        today = pd.Timestamp.today().floor("1d")
        number_of_days = (today - last_fetched_date).days
        for i in range(number_of_days + 2):
            date = last_fetched_date + pd.Timedelta(days=i)
            my_sql_data = self.get_data_per_date(date)
            self.insert_to_mysql(my_sql_data)
            
    def get_data_per_date(self, date=None):
        all_orders = []
        all_meals = []
        all_reviews = []
        for resto in self.restaurants:
            last_fetched = pd.Timestamp.today(tz=TIMEZONE).floor("1d")
            resto = Restaurant.objects.get(resto_id=resto['id'])
            resto_orders, resto_meals, resto_reviews = self._fetch_restaurant_data(resto, date)
            all_meals.extend(resto_meals)
            all_orders.extend(resto_orders)
            all_reviews.extend(resto_reviews)
        return [MySqlInput(Order, all_orders), MySqlInput(Meal, all_meals), MySqlInput(Review, all_reviews)]

    def insert_to_mysql(self, my_sql_input):
        for inp in my_sql_input:
            inp.model.objects.bulk_create(inp.data, ignore_conflicts=True)
        

    def _get_last_fetched(self):
        a = self._mysqlcursor.execute("SELECT MAX(date) from orders;")
        return self._mysqlcursor.fetchone()[0]


DELIVEROO = Provider(PROVIDER_NAME, DeliverooApi)
