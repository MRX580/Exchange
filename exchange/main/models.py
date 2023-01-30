from django.db import models
from django.urls import reverse


class NameCoin(models.Model):
    name_coin = models.CharField(verbose_name='NameCoin', max_length=10)
    choice_status = models.CharField(verbose_name='Status', max_length=15)
