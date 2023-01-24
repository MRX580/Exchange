from django.urls import path
from .views import *
from django.contrib.auth import views as authViews
from . import views

urlpatterns = [
    path('', index),
]