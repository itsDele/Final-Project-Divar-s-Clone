from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler403, handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , include('Main.urls'), name='Main')
]

if settings.DEBUG:  # Serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = 'Main.views.custom_403'
handler404 = 'Main.views.custom_404'