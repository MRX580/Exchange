from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='blog'),
    path('<int:pk>', blog, name='blog'),
]