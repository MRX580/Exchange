from django.db import models
from django.contrib.auth.models import AbstractUser
#
# class MeinAuth(models.Model):
#     mein_auth = models.ForeignKey(AbstractUser, on_delete=models.CASCADE)
#     api_key = models.CharField(verbose_name='Api', max_length=64)
#     secret_key = models.CharField(verbose_name='Secret', max_length=64)


class Signup(models.Model):
    name = models.CharField(verbose_name='Name', max_length=15)
    email = models.CharField(verbose_name='Email', max_length=50)
    password = models.CharField(verbose_name='Password', max_length=15)
    api_key = models.CharField(verbose_name='Api', max_length=64)
    secret_key = models.CharField(verbose_name='Secret', max_length=64)


class Signin(models.Model):
    email = models.CharField(verbose_name='Email', max_length=50)
    password = models.CharField(verbose_name='Password', max_length=15)
