from app.controllers import *
from django.conf.urls import url, include
from rest_framework import routers


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^login', login),
    url(r'^orders_count', orders_counts),
    url(r'^meals_count', meals_count),
    url(r'^last_orders', last_orders),
    url(r'^top_numbers', top_numbers)
]