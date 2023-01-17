from .models import Signup, Signin
from django.forms import ModelForm, TextInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control',
            }),
            'email': TextInput(attrs={
                'class': 'form-control',
            }),
            'password': TextInput(attrs={
                'id': 'userPassword',
                'type': 'password',
                'class': 'form-control',
            }),
            'first_name': TextInput(attrs={
                'class': 'form-control',
            }),
            'last_name': TextInput(attrs={
                'class': 'form-control',
            }),
        }


class LoginForm(ModelForm):
    class Meta:
        model = Signin
        fields = ['email', 'password']
        widgets = {
            'email': TextInput(attrs={
                'class': 'form-control',
            }),
            'password': TextInput(attrs={
                'id': 'userPassword',
                'type': 'password',
                'class': 'form-control',
            }),
        }
