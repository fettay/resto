from rest_framework import serializers
from django.contrib.auth.models import User
from app.models import Order


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ['order_id', 'order_number', 'amount', 'date',
                  'restaurant', 'status', 'service']
