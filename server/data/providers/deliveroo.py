from data.core import ProviderApi, LoginError, Provider
from app.models import Order, Credentials, Meal

from tqdm import tqdm
import pandas as pd

import requests
import json
import pprint
from datetime import datetime
from urllib.parse import quote
from getpass import getpass

LOGIN_URL = "https://restaurant-hub.deliveroo.net/api/session"
RESTO_URL = "https://restaurant-hub.deliveroo.net/api/restaurants/{restaurant_id}"
ORDERS_URL = RESTO_URL + "/orders?date={date}&end_date={date}&starting_after={start_after}&sort_date={sort_date}&with_summary=no"
ITEMS_URL = RESTO_URL + "/order_items?start_date={date}&end_date={date}&group_modifiers=true"
TIMEZONE = "Europe/Paris"
PROVIDER_NAME = 'Deliveroo'


class DeliverooApi(ProviderApi):

    def __init__(self, user):
        self._token = None
        self.restaurants = None
        self._mysqlcursor = None 
        super().__init__(user)

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
        return res

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

    def _format_meal(self, order, restaurant, date):
        meal_dict = {'category': order['category_name'],
                      'title': order['name'], 
                      'date': pd.Timestamp(date, tz=TIMEZONE).floor("1d").to_pydatetime(),
                      'provider': PROVIDER_NAME,
                      'restaurant': restaurant,
                      'owner_id': self._user,
                      'quantity': order['quantity']}
        
        return Meal(**meal_dict)

    def _fetch_restaurant_data(self, restaurant_id, date, restaurant_name):
        last_timestamp = None
        last_fetched_id = None
        all_orders = []
        while True:
            date_str = date.strftime("%Y-%m-%d")
            if last_fetched_id is None:
                url = ORDERS_URL.format(restaurant_id=restaurant_id, start_after="",
                                            date=date_str, sort_date="")
            else:
                timestamp_str = quote(str(last_timestamp).replace(" ", "T").replace("+", " "))
                url = ORDERS_URL.format(restaurant_id=restaurant_id, start_after=last_fetched_id,
                                            date=date_str, sort_date=timestamp_str)

            orders = requests.get(url, headers={'authorization': self._token}).json()
            new_orders = [self._format_order(o, restaurant_name) for o in orders['orders']]

            if len(new_orders) == 0 or (last_timestamp is not None and new_orders[-1].order_id == all_orders[-1].order_id):
                break 

            all_orders.extend(new_orders)
            last_fetched_id = all_orders[-1].order_id
            last_timestamp = all_orders[-1].date
        
        items_sold_url = ITEMS_URL.format(restaurant_id=restaurant_id, date=date_str)
        meals = requests.get(items_sold_url, headers={'authorization': self._token}).json()
        meals = [self._format_meal(m, restaurant_name, date) for m in meals]
        return all_orders, meals

    def onboard(self, ndays):
        user_info = self.login()
        splitted_name = user_info['name'].split(' ')
        self._user.first_name = splitted_name[0]

        if len(splitted_name) > 1:
            self._user.last_name = " ".join(splitted_name[1:])
    
        self._user.save()
        today = pd.Timestamp.today().floor("1d")
        print('Hey %s, we are loading your data' % (self._user.first_name))
        for i in tqdm(range(0, ndays + 1), total=ndays):
            date = today - pd.Timedelta(days=i)
            all_orders, meals = self.get_data_per_date(date)
            self.insert_to_mysql(all_orders, meals)
    
    def update_data(self):
        last_fetched_date = self._get_last_fetched()
        today = pd.Timestamp.today().floor("1d")
        number_of_days = (today - last_fetched_date).days
        for i in range(number_of_days + 2):
            date = last_fetched_date + pd.Timedelta(days=i)
            orders, meals = self.get_data_per_date(date)
            self.insert_to_mysql(orders, meals)
            
    def get_data_per_date(self, date=None):
        all_orders = []
        all_meals = []
        for resto in self.restaurants:
            last_fetched = pd.Timestamp.today(tz=TIMEZONE).floor("1d")
            resto_orders, resto_meals = self._fetch_restaurant_data(resto['id'], date, resto['name'])
            all_meals.extend(resto_meals)
            all_orders.extend(resto_orders)
        return all_orders, all_meals

    def insert_to_mysql(self, orders_list, meals_list):
        _ = Order.objects.bulk_create(orders_list, ignore_conflicts=True)
        _ = Meal.objects.bulk_create(meals_list, ignore_conflicts=True)
        

    def _get_last_fetched(self):
        a = self._mysqlcursor.execute("SELECT MAX(date) from orders;")
        return self._mysqlcursor.fetchone()[0]


DELIVEROO = Provider(PROVIDER_NAME, DeliverooApi)
