from django.urls import path
from .views import get_chart

urlpatterns = [
    path('', get_chart, name='chart'),
]
