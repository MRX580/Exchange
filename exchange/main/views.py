from django.shortcuts import render, redirect, HttpResponse
from .forms import UserRegisterForm, UserLoginForm
from binance.client import Client
from .models import *
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ValidationError


def welcome(request):
    return render(request, 'main.html')


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегестрировались')
            return redirect('account')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'sign_up.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('account')
        else:
            messages.error(request, 'Ошибка авторизации')
    else:
        form = UserLoginForm()
    return render(request, 'sing_in.html', {'form': form})


def account(request):
    your_models = User.objects.all()
    apis = []
    for model in your_models:
        apis.append(model.first_name)
    col_vo_strock = len(apis) - 1
    api = your_models[col_vo_strock]
    api_key_get = api.first_name
    secret_key_get = api.last_name
    client = Client(api_key_get, secret_key_get)
    info = client.get_account().get('balances')
    name_coins = []
    col_vo_coins = []
    price = []
    changes = []
    for i in info:
        if float(i.get('free')) > 0:
            name_coins.append(i.get('asset'))
            col_vo_coins.append(float(i.get('free')))
            coin = i.get('asset')
            if coin == 'USDT':
                cost = round(float(client.get_symbol_ticker(symbol='USDTUAH').get('price')) / 40, 2)
                price.append(str(cost) + ' $')
                change = round(float(client.get_ticker(symbol='USDTUAH').get('priceChangePercent')), 2)
                if change > 0:
                    changes.append('+ ' + str(change) + ' %')
                else:
                    changes.append(str(change) + ' %')
            elif coin == 'UAH':
                cost = round(float(client.get_symbol_ticker(symbol='USDTUAH').get('price')), 2)
                price.append(str(cost) + ' ₴')
                change = round(float(client.get_ticker(symbol='USDTUAH').get('priceChangePercent')), 2)
                if change > 0:
                    changes.append('+ ' + str(change) + ' %')
                else:
                    changes.append(str(change) + ' %')
            elif coin == 'LUNC':
                cost = float(client.get_symbol_ticker(symbol='LUNCBUSD').get('price'))
                price.append(str(cost) + ' $')
                change = round(float(client.get_ticker(symbol='LUNCBUSD').get('priceChangePercent')), 2)
                if change > 0:
                    changes.append('+ ' + str(change) + ' %')
                else:
                    changes.append(str(change) + ' %')
            else:
                cost = round(float(client.get_symbol_ticker(symbol=coin + 'USDT').get('price')), 2)
                price.append(str(cost) + ' $')
                change = round(float(client.get_ticker(symbol=coin + 'USDT').get('priceChangePercent')), 2)
                if change > 0:
                    changes.append('+ ' + str(change) + ' %')
                else:
                    changes.append(str(change) + ' %')
    return render(request, 'your_accaunt.html',
                  {'name_coin': name_coins, 'col_vo_coin': col_vo_coins, 'price': price, 'changes': changes})

