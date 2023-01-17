from django.shortcuts import render, redirect, HttpResponse
from .forms import UserRegisterForm, LoginForm
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



def signin(request):
    error = ''
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            login_form.save()
            return redirect('/wallet/profile')
        else:
            error = 'Form is not valid'
    form = LoginForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'sing_in.html', context)


def account_for_login(request):
    email_signup = []
    password_signup = []
    email_login = []
    password_login = []
    models_for_signup = Signup.objects.all()
    models_for_login = Signin.objects.all()
    for model_for_email_signup in models_for_signup:
        email_signup.append(model_for_email_signup.email)
    for model_for_password_signup in models_for_signup:
        password_signup.append(model_for_password_signup.password)
    for model_for_email_login in models_for_login:
        email_login.append(model_for_email_login.email)
    for model_for_password_login in models_for_login:
        password_login.append(model_for_password_login.password)
    len_login = len(email_login) - 1
    general = models_for_login[len_login]
    email_for_login = general.email
    password_for_login = general.password
    for all_form_signup in email_signup:
        for examination_on_password in password_signup:
            if email_for_login == all_form_signup:
                if password_for_login == examination_on_password:
                    api_key = Signup.objects.get(email=email_for_login).api_key
                    secret_key = Signup.objects.get(email=email_for_login).secret_key
                    client = Client(api_key, secret_key)
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
                                change = round(float(client.get_ticker(symbol=coin + 'USDT').get('priceChangePercent')),
                                               2)
                                if change > 0:
                                    changes.append('+ ' + str(change) + ' %')
                                else:
                                    changes.append(str(change) + ' %')
                    return render(request, 'your_accaunt.html',
                                  {'name_coin': name_coins, 'col_vo_coin': col_vo_coins, 'price': price,
                                   'changes': changes})


def account(request):
    your_models = User.objects.all()
    apis = []
    for model in your_models:
        apis.append(model.password2)
    col_vo_strock = len(apis) - 1
    api = your_models[col_vo_strock]
    api_key_get = api.password2
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

