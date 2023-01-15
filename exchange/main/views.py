from django.shortcuts import render, redirect, HttpResponse
from .forms import TaskForm, LoginForm
from binance.client import Client
from .models import *
from django.contrib import messages
from django.core.exceptions import ValidationError


def welcome(request):
    return render(request, 'main.html')


def Sing_up(request):
    error = ''
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            api = len(form.cleaned_data['api_key'])
            secret = len(form.cleaned_data['secret_key'])
            email = form.cleaned_data['email']
            if Signup.objects.filter(email__iexact=email).exists():
                messages.error(request, "Such mail exists")
            elif Signup.objects.filter(api_key__iexact=form.cleaned_data['api_key']).exists():
                messages.error(request, "Such Api Key exists")
            elif Signup.objects.filter(secret_key__iexact=form.cleaned_data['secret_key']).exists():
                messages.error(request, "Such Secret Key exists")
            elif api < 64 or api > 64:
                messages.error(request, "Api Key not valid")
            elif secret < 64 or secret > 64:
                messages.error(request, "Secret Key not valid")
            else:
                form.save()
                return redirect('/your_account')
        else:
            error = 'Form is not valid'
    form = TaskForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'sign_up.html', context)


def signin(request):
    error = ''
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            login_form.save()
            return redirect('/profile')
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
                                change = round(float(client.get_ticker(symbol=coin + 'USDT').get('priceChangePercent')), 2)
                                if change > 0:
                                    changes.append('+ ' + str(change) + ' %')
                                else:
                                    changes.append(str(change) + ' %')
                    return render(request, 'your_accaunt.html', {'name_coin': name_coins, 'col_vo_coin': col_vo_coins, 'price': price, 'changes': changes})


def choice(request):
    return render(request, 'choice.html')


def account(request):
    your_models = Signup.objects.all()
    apis = []
    for model in your_models:
        apis.append(model.api_key)
    col_vo_strock = len(apis) - 1
    api = your_models[col_vo_strock]
    api_key_get = api.api_key
    secret_key_get = api.secret_key
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
    return render(request, 'your_accaunt.html', {'name_coin': name_coins, 'col_vo_coin': col_vo_coins, 'price': price, 'changes': changes})
