from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('data/', include('data.urls')),
    path('device/', include('device.urls')),
    path('user/', include('user.urls')),
    path('auth/', include('drf_social_oauth2.urls', namespace='drf')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
