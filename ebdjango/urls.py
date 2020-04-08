from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
   url(r'', include('main.urls')), 
   url(r'^admin/', admin.site.urls),
   path('tinymce/', include('tinymce.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
