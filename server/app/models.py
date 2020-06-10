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
    service = models.CharField(max_length=50)

