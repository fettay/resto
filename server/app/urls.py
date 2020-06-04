from django.urls import path

from .controllers import home

urlpatterns = [
    path('', home, name='home')
]