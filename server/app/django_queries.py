from app.models import Order, Meal, Review
from app.core import Aggregator

from django.db.models import Count, Sum, Avg
from django.contrib.auth.models import User
import pandas as pd


def get_orders_count(user: User, aggregator: Aggregator):
    qs = Order.objects.filter(owner_id=user.id).extra({'created_day':"%s(date)" % aggregator.value}).\
    values('created_day').\
    annotate(count=Count('*'))
    return qs


def get_sales_count(user: User, aggregator: Aggregator):
    qs = Order.objects.filter(owner_id=user.id).extra({'created_day':"%s(date)" % aggregator.value}).\
    values('created_day').\
    annotate(count=Sum('amount'))
    return qs


def get_avg_sales(user: User, aggregator: Aggregator):
    qs = Order.objects.filter(owner_id=user.id).extra({'created_day':"%s(date)" % aggregator.value}).\
    values('created_day').\
    annotate(count=Avg('amount'))
    return qs


def get_avg_review(user: User, aggregator: Aggregator):
    qs = Review.objects.filter(owner_id=user.id).extra({'created_day':"%s(date)" % aggregator.value}).\
    values('created_day').\
    annotate(count=Avg('rating'))
    return qs


def get_last_orders(user: User):
    qs = Order.objects.filter(owner_id=user.id).order_by('-date')[:10]
    return qs

def get_meals_count(user: User, top: int):
    if top is not None:
        qs = Meal.objects.filter(owner_id=user.id)\
                        .values('title')\
                        .annotate(count=Sum('quantity'))\
                        .order_by('-count')[:top]
    else:
        qs = Meal.objects.filter(owner_id=user.id)\
                        .values('title')\
                        .annotate(count=Sum('quantity')).order_by('-count')

    return qs

def get_orders_variation(user: User):
    orders_counts = pd.DataFrame(orders_counts)
