from rest_framework import serializers
from django.contrib.auth.models import User
from app.models import Order, Meal, Restaurant


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['resto_id', 'name']


class OrderSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer()
    class Meta:
        model = Order
        fields = ['order_id', 'restaurant', 'order_number', 'amount', 'date', 'status']
        depth = 1


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ['owner_id', 'restaurant', 'category', 'title',
                  'date', 'quantity', 'provider']

