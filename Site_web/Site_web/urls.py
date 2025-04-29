from django.contrib import admin
from django.urls import path, include 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('', include('Client.urls')),
    path('', include('Superviseur.urls')),
    path('', include('Public_App.urls')),
    path('', include('Authentication.urls')),
    path('api/', include('REST_API.urls')),
]

# Ajouter ceci pour servir les fichiers médias en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)