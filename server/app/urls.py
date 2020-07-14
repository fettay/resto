from app.controllers import *
from django.conf.urls import url, include
from rest_framework import routers
from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm


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
    url(r'^top_numbers', top_numbers),
    url(r'^sales_total', sales_total),
    url(r'^orders_per_weekday', orders_per_weekday),
    url(r'^orders_resto_count', orders_resto_count),
    url(r'^sales_resto_total', sales_resto_total),
    url(r'^sales_resto_average', sales_resto_average),
    url(r'^password_reset', reset_password),
    url(r'^reset_password', reset_password_request_token),
    url(r'^confirm_reset_password', reset_password_confirm)
]