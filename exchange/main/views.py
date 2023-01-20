from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm
from binance.client import Client
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('home')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = UserRegisterForm()
    return render(request, 'sign_up.html', {'form': form})


def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear {user}, please go to you email {to_email} inbox and click on \
            received activation link to confirm and complete the registration. Note: Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('signin')
    else:
        messages.error(request, 'Activation link is invalid!')

    return redirect('home')


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
    return render(request, 'your_accaunt.html', {'name_coin': name_coins, 'col_vo_coin': col_vo_coins, 'price': price, 'changes': changes})

