from app.models import Order, Meal, Review
from app.core import Aggregator

from django.db.models import Count, Sum, Avg
from django.contrib.auth.models import User
import pandas as pd

from datetime import datetime


def get_orders_count(user: User, aggregator: Aggregator):
    qs = Order.objects.filter(owner=user.id).extra({'created_day':"%s(date)" % aggregator.value}).\
    values('created_day').\
    annotate(count=Count('*'))
    return qs


def get_sales_count(user: User, aggregator: Aggregator):
    qs = Order.objects.filter(owner=user.id).extra({'created_day':"%s(date)" % aggregator.value}).\
    values('created_day').\
    annotate(count=Sum('amount'))
    return qs


def get_avg_sales(user: User, aggregator: Aggregator):
    qs = Order.objects.filter(owner=user.id).extra({'created_day':"%s(date)" % aggregator.value}).\
    values('created_day').\
    annotate(count=Avg('amount'))
    return qs


def get_avg_review(user: User, aggregator: Aggregator):
    qs = Review.objects.filter(owner=user.id).extra({'created_day':"%s(date)" % aggregator.value}).\
    values('created_day').\
    annotate(count=Avg('rating'))
    return qs


def get_last_orders(user: User):
    qs = Order.objects.filter(owner=user.id).order_by('-date')[:10]
    return qs

def get_meals_count(user: User, top: int):
    if top is not None:
        qs = Meal.objects.filter(owner=user.id)\
                        .values('title')\
                        .annotate(count=Sum('quantity'))\
                        .order_by('-count')[:top]
    else:
        qs = Meal.objects.filter(owner=user.id)\
                        .values('title')\
                        .annotate(count=Sum('quantity')).order_by('-count')

    return qs

def get_sales_total(user: User, start_date: str=None, end_date: str=None):
    qs = Order.objects.filter(owner=user.id)
    if start_date is not None:
        qs = qs.filter(date__gte=start_date)
    
    if end_date is not None:
        qs = qs.filter(date__lte=end_date)
    
    qs = qs.values('restaurant__name').annotate(count=Sum('amount'))
    return qs


def get_orders_per_weekday(user: User, start_date: str=None, end_date: str=None):
    qs = Order.objects.filter(owner=user.id)
    if start_date is not None:
        qs = qs.filter(date__gte=start_date)
    
    if end_date is not None:
        qs = qs.filter(date__lte=end_date)
    
    qs = qs.values('restaurant__name', 'date__week_day').annotate(count=Count('*'))
    return qs


def _get_aggregation_by_resto(user: User, aggregator: Aggregator, start_date: str=None, end_date: str=None):
    qs = Order.objects.filter(owner=user.id)
    if start_date is not None:
        qs = qs.filter(date__gte=start_date)
    
    if end_date is not None:
        qs = qs.filter(date__lte=end_date)
    qs = qs.extra({'created_day':"%s(date)" % aggregator.value}).\
            values('restaurant__name', 'created_day')
    return qs


def get_orders_resto_count(user: User, aggregator: Aggregator, start_date: str=None, end_date: str=None):
    qs = _get_aggregation_by_resto(user, aggregator, start_date, end_date)
    return qs.annotate(count=Count('*'))


def get_sales_resto_total(user: User, aggregator: Aggregator, start_date: str=None, end_date: str=None):
    qs = _get_aggregation_by_resto(user, aggregator, start_date, end_date)
    return qs.annotate(count=Sum('amount'))


def get_sales_resto_average(user: User, aggregator: Aggregator, start_date: str=None, end_date: str=None):
    qs = _get_aggregation_by_resto(user, aggregator, start_date, end_date)
    return qs.annotate(count=Avg('amount'))

