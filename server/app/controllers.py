from app.serializers import UserSerializer, OrderSerializer
from app.django_queries import *
from app.core import Aggregator
from app.stats import compute_evolution
from app.constants import TIMEZONE, DJANGO_WEEKDAYS

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from datetime import datetime
import pytz


def _parse_input_date(date_str):
    if date_str is None:
        return None
    
    tz = pytz.timezone(TIMEZONE)

    try:
        return tz.localize(datetime.strptime(date_str , "%Y-%m-%d"))
    except Exception:
        return None


@api_view(['POST'])
def login(request, format=None):
    if request.user.is_authenticated:
        return Response(UserSerializer(request.user).data)
    
    user = authenticate(username=request.data['email'], password=request.data['password'])
    if user is None:
        return Response({'error': 'User cannot be found'}, 401)

    token, created = Token.objects.get_or_create(user=user)
    response_data = UserSerializer(user).data
    response_data['token'] = token.key
    return Response(response_data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def orders_counts(request, format=None):
    query = get_orders_count(request.user, Aggregator.DAY)
    data = query.all()
    return Response(data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def sales_total(request, format=None):
    start_date = _parse_input_date(request.GET.get('start_date', None))
    end_date = _parse_input_date(request.GET.get('end_date', None))
    query = get_sales_total(request.user, start_date, end_date)
    data = query.all()
    return Response(data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def orders_per_weekday(request, format=None):
    start_date = _parse_input_date(request.GET.get('start_date', None))
    end_date = _parse_input_date(request.GET.get('end_date', None))
    query = get_orders_per_weekday(request.user, start_date, end_date)
    data = query.all()
    formatted = map(lambda value: {'count': value['count'],
                                   'day': DJANGO_WEEKDAYS[value['date__week_day']],
                                   'restaurant': value['restaurant__name']},
                    data)
    return Response(formatted)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def orders_resto_count(request, format=None):
    start_date = _parse_input_date(request.GET.get('start_date', None))
    end_date = _parse_input_date(request.GET.get('end_date', None))
    query = get_orders_resto_count(request.user, Aggregator.DAY, start_date, end_date)
    data = query.all()
    return Response(data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def sales_resto_total(request, format=None):
    start_date = _parse_input_date(request.GET.get('start_date', None))
    end_date = _parse_input_date(request.GET.get('end_date', None))
    query = get_sales_resto_total(request.user, Aggregator.DAY, start_date, end_date)
    data = query.all()
    return Response(data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def sales_resto_average(request, format=None):
    start_date = _parse_input_date(request.GET.get('start_date', None))
    end_date = _parse_input_date(request.GET.get('end_date', None))
    query = get_sales_resto_average(request.user, Aggregator.DAY, start_date, end_date)
    data = query.all()
    return Response(data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def last_orders(request, format=None):
    query = get_last_orders(request.user)
    data = query.all()
    serialized_list = [OrderSerializer(order, context={'request': request}).data for order in data]
    return Response(serialized_list)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def meals_count(request, format=None):
    top = request.GET.get('top', None)
    if top is not None:
        top = int(top)
    query = get_meals_count(request.user, top)
    data = query.all()
    return Response(data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def top_numbers(request, format=None):
    data_list = {'orders': (get_orders_count(request.user, Aggregator.DAY).all(), 'sum'),
                 'sales': (get_sales_count(request.user, Aggregator.DAY).all(), 'sum'),
                 'sales_avg': (get_avg_sales(request.user, Aggregator.DAY).all(), 'mean'),
                 'reviews': (get_avg_review(request.user, Aggregator.DAY).all(), 'mean')}
    data = {k: compute_evolution(v[0], 7, 'created_day', v[1]) for k, v in data_list.items()}
    data = {k: {'value': value, 'change': change} for k, (value, change) in data.items()}
    return Response(data)
