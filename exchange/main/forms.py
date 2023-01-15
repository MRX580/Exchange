from .models import Signup, Signin
from django.forms import ModelForm, TextInput


class TaskForm(ModelForm):
    class Meta:
        model = Signup
        fields = ['name', 'email', 'password', 'api_key', 'secret_key']
        widgets = {
            'name': TextInput(attrs={
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
            'api_key': TextInput(attrs={
                'class': 'form-control',
            }),
            'secret_key': TextInput(attrs={
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
