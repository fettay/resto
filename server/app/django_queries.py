from app.models import Order
from app.core import Aggregator

from django.db.models import Count
from django.contrib.auth.models import User


def get_orders_count(user: User, aggregator: Aggregator):
    qs = Order.objects.filter(owner_id=user.id).extra({'created_day':"%s(date)" % aggregator.value}).\
    values('created_day').\
    annotate(count=Count('*'))
    return qs


def get_last_orders(user: User):
    qs = Order.objects.filter(owner_id=user.id).order_by('-date')[:10]
    return qs
