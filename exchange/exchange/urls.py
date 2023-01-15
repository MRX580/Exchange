from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('application.urls')),
    path('chart/', include('charts.urls')),
    path('wallet/', include('main.urls')),
]
