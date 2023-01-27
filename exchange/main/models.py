from django.db import models


class NameCoin(models.Model):
    name_coin = models.CharField(verbose_name='NameCoin', max_length=10)
