from django.urls import path
from .views import *

urlpatterns = [
    path('', welcome),
    path('your_account/', account, name='account'),
    path('signup/', Sing_up, name='signup'),
    path('signin/', signin, name='signin'),
    path('profile/', account_for_login)
]