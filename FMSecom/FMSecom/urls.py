
from django.contrib import admin
from django.urls import include, path

#imagenes
from django.conf import settings
from django.conf.urls.static import static
from core import views

# Se añade a urlpatterns los parametros para buscar las imagenes correctamente
urlpatterns = [
    path('admin/', admin.site.urls),
    path('tienda/', include('tienda.urls', namespace='tienda')),
    path('autenticacion/', include('autenticacion.urls', namespace='autenticacion')),
    path('', include('core.urls')),
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
