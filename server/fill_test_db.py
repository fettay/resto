import django
import os
import pandas as pd


os.environ['DJANGO_SETTINGS_MODULE'] = "resto_server.settings"
django.setup()


from django.contrib.auth.models import User
from app.models import Order


def create_users():
    try:
        user = User.objects.get(username='ericbg@gmail.com', email='ericbg@gmail.com', 
                                            first_name="Eric", last_name="May")
    except User.DoesNotExist:
        user = User.objects.create_user(id=1, username='ericbg@gmail.com', email='ericbg@gmail.com', password='password',
                                            first_name="Eric", last_name="May") 
        user.save()

def create_orders():
    df_orders = pd.read_csv('data/orders.csv') 
    orders_list = []
    owner = User.objects.get(pk=1)
    for _, row in df_orders.iterrows():
        row['owner_id'] = owner
        row['order_id'] = row['orderid']
        del row['orderid']

        orders_list.append(Order(**row))
    try:
        Order.objects.bulk_create(orders_list)
    except django.db.utils.IntegrityError:
        pass

if __name__ == "__main__":
     create_users()
     create_orders()
   
