from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('', include('application.urls')),
    path('chart/', include('charts.urls')),
    path('blog/', include('blog.urls')),
    path('wallet/', include('main.urls')),
]