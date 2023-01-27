from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import NameCoin
from django.forms import ModelForm, TextInput


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label="Имя пользователя", widget=forms.TextInput(attrs={"class": 'form-control'}))
    email = forms.EmailField(label='Почта', widget=forms.EmailInput(attrs={"class": 'form-control'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"class": 'form-control'}))
    password2 = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput(attrs={"class": 'form-control'}))
    first_name = forms.CharField(label="Апи ключ", widget=forms.TextInput(attrs={"class": 'form-control'}))
    last_name = forms.CharField(label="Секретный ключ", widget=forms.TextInput(attrs={"class": 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя:", widget=forms.TextInput(attrs={"class": 'form-control'}))
    password = forms.CharField(label="Пароль:", widget=forms.PasswordInput(attrs={"class": 'form-control'}))


class NameCoinForm(ModelForm):
    class Meta:
        model = NameCoin
        fields = ['name_coin']
        widgets = {
            'name_coin': forms.TextInput(attrs={
                'type': "search",
                'placeholder': "Name coin",
                'aria-label': "Search",
                'size': "20",
                'style': "border-radius: 3px;"
            }),
        }



