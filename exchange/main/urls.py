from django.urls import path
from .views import *
from django.contrib.auth import views as authViews
from . import views

urlpatterns = [
    path('your_account/', account, name='account'),
    path('signup/', user_register, name='signup'),
    path('signin/', user_login, name='signin'),
    path('exit/', authViews.LogoutView.as_view(next_page='home'), name='exit'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('history_trade_spot/', history_spot, name='history_spot'),
    path('enter/', name_coin, name='enter'),
    path('spot/', spot, name='spot')
]