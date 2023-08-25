from django.contrib import admin

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from authentication.utils import schema_view

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path("", include('users.urls'), name='users'),
    path("auth/", include('authentication.urls'), name='authentication'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
