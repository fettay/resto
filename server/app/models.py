from django.db import models
from django.contrib.auth.models import User


class Restaurant(models.Model):
    resto_id = models.CharField(max_length=150)
    owner = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=150)
    latitude = models.FloatField()
    longitude = models.FloatField()
    provider = models.CharField(max_length=50)

    class Meta:
        unique_together = (("owner", "resto_id", "provider"),)


class Order(models.Model):
    order_id = models.CharField(max_length=150, primary_key=True)
    owner = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    order_number = models.IntegerField()
    amount = models.FloatField()
    date = models.DateTimeField()
    restaurant = models.ForeignKey(to=Restaurant, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=50)
    provider = models.CharField(max_length=50)


class Credentials(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    provider = models.CharField(max_length=50)
    credentials = models.CharField(max_length=200)

    class Meta:
        unique_together = (("owner", "provider"),)


class Meal(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    order = models.ForeignKey(to=Order, on_delete=models.DO_NOTHING)
    category = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    quantity = models.IntegerField()
    provider = models.CharField(max_length=50)


class Review(models.Model):
    order = models.OneToOneField(to=Order, on_delete=models.DO_NOTHING, primary_key=True)
    owner = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    restaurant = models.ForeignKey(to=Restaurant, on_delete=models.DO_NOTHING)
    date = models.DateTimeField()
    comment = models.TextField()
    rating = models.IntegerField()
    provider = models.CharField(max_length=50)