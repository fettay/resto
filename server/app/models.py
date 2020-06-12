from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    order_id = models.CharField(max_length=150, primary_key=True)
    owner_id = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    order_number = models.IntegerField()
    amount = models.FloatField()
    date = models.DateTimeField()
    restaurant = models.CharField(max_length=150)
    status = models.CharField(max_length=50)
    provider = models.CharField(max_length=50)


class Credentials(models.Model):
    owner_id = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    provider = models.CharField(max_length=50)
    credentials = models.CharField(max_length=200)

    class Meta:
        unique_together = (("owner_id", "provider"),)


class Meal(models.Model):
    owner_id = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    restaurant = models.CharField(max_length=150)
    category = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    quantity = models.IntegerField()
    provider = models.CharField(max_length=50)

    class Meta:
        unique_together = (("owner_id", "title", "date", "provider"),)