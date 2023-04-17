from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from .settings import DEBUG, MEDIA_URL, MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('', include('application.urls')),
    path('blog/', include('blog.urls')),
    path('wallet/', include('main.urls')),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)