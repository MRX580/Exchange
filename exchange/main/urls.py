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
]