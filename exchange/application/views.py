import random

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import JsonResponse
from rest_framework import generics, permissions
from binance.client import Client
from .serializers import MyModelSerializer
from .models import Coins
from .forms import UserRegisterForm, UserLoginForm
from datetime import datetime, timedelta

API_B = 'uxq5ys5QYsXtzjlurz2qEXgsEd522wF6uEfntReadmjjRcC83BUrw6mIkZ1G6zx5'
Secret_B = 'dmSOOwuzHvXcDgzi4EvhceZi48uX2eKyEPuXQQPsyudH35SQCKaGEkCFLqTVWc03'


class CoinsListView(generics.ListCreateAPIView):
    queryset = Coins.objects.all()
    serializer_class = MyModelSerializer
    permission_classes = (permissions.IsAdminUser,)


class CoinDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Coins.objects.all()
    serializer_class = MyModelSerializer
    permission_classes = (permissions.IsAdminUser,)


class BinanceData:
    def __init__(self, client: Client):
        self.client = client

    def divine_number(self, number_str: str, length: int = 0) -> str:
        left_side = f'{int(number_str.split(".")[0]):,}'
        if length >= 1:
            right_side = number_str.split(".")[1][:length]
            return f'{left_side}.{right_side}'
        return left_side

    def coin(self, symbol: str, length: int = 0):
        resault = str(self.client.get_symbol_ticker(symbol=symbol)['price'])
        return '$' + self.divine_number(resault, length)

    def volume(self, symbol):
        resault = self.client.get_ticker(symbol=symbol)['volume']
        return self.divine_number(resault, 0)

    def quoteVolume(self, symbol):
        resault = self.client.get_ticker(symbol=symbol)['quoteVolume']
        return '$' + self.divine_number(resault, 2)

    def hours24(self, symbol):
        resault = self.client.get_ticker(symbol=symbol)['priceChangePercent']
        return self.divine_number(resault, 5) + '%'


def home(request):
    client = BinanceData(Client(API_B, Secret_B))
    coins = ['BTC', 'ETH', 'XRP', 'ADA']
    currency = 'USDT'
    params = ['price', 'volume', 'full_name', 'procent_change', 'quote_volume']
    html_tags = ['price', 'name', 'volume', 'procent_change', 'quote_volume']

    data = {
        'BTC': {'price': client.coin('BTCUSDT', 3), 'volume': client.volume('BTCUSDT'), 'full_name': 'Bitcoin BTC',
                'procent_change': client.hours24('BTCUSDT'), 'quote_volume': client.quoteVolume('BTCUSDT'), 'html_tag':
            {'price': 'BTC_price', 'name': 'BTC_name', 'volume': 'BTC_volume', 'procent_change': 'BTC_procent_change',
             'quote_volume': 'BTC_quote_volume'}},
        'ETH': {'price': client.coin('ETHUSDT', 3), 'volume': client.volume('ETHUSDT'), 'full_name': 'Etherium ETH',
                'procent_change': client.hours24('ETHUSDT'), 'quote_volume': client.quoteVolume('ETHUSDT'), 'html_tag':
            {'price': 'ETH_price', 'name': 'ETH_name', 'volume': 'ETH_volume', 'procent_change': 'ETH_procent_change',
             'quote_volume': 'ETH_quote_volume'}},
        'XRP': {'price': client.coin('XRPUSDT', 5), 'volume': client.volume('XRPUSDT'), 'full_name': 'Ripple XRP',
                'procent_change': client.hours24('XRPUSDT'), 'quote_volume': client.quoteVolume('XRPUSDT'), 'html_tag':
            {'price': 'XRP_price', 'name': 'XRP_name', 'volume': 'XRP_volume', 'procent_change': 'XRP_procent_change',
             'quote_volume': 'XRP_quote_volume'}},
        'ADA': {'price': client.coin('ADAUSDT', 5), 'volume': client.volume('ADAUSDT'), 'full_name': 'Cardano ADA',
                'procent_change': client.hours24('ADAUSDT'), 'quote_volume': client.quoteVolume('ADAUSDT'), 'html_tag':
                    {'price': 'ADA_price', 'name': 'ADA_name', 'volume': 'ADA_volume',
                     'procent_change': 'ADA_procent_change',
                     'quote_volume': 'ADA_quote_volume'}}
    }
    if is_ajax(request=request):
        return JsonResponse(data, status=200)
    return render(request, 'application/index.html', {'coins': data})


def user_logout(request):
    logout(request)
    return redirect('login')


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                if form.cleaned_data['remember_me']:
                    request.session.set_expiry(14 * 24 * 60 * 60)  # Two weeks
                else:
                    request.session.set_expiry(0)  # When the browser closes
                return redirect('home')
        else:
            messages.error(request, 'Ошибка авторизации')
    else:
        form = UserLoginForm()
    return render(request, 'application/login.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # сохраняем форму
            login(request, user)  # сразу заходим в аккаунт
            messages.success(request, 'Вы успешно зарегестрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'application/login.html', {'form': form})
