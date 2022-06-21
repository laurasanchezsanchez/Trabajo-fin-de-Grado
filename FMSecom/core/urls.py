from django.urls import path

from . import views

from . views import indexListView
from . views import ContactView
from django.conf import settings
from django.conf.urls.static import static
app_name = 'core'

#arreglar barra tutoriales
urlpatterns = [
    path('', indexListView.as_view(), name='index'),
    path('base/', views.baseView, name='base'),
    path('tutoriales', views.tutoriales, name='tutoriales'),
    path('instalaciones/', views.instalaciones, name='instalaciones'),
    path('receptora', views.receptora, name='receptora'),
    path('contacto/', views.ContactView.as_view(), name='contacto'),
    path('manuales/', views.manualesView, name='manuales'),
    path('tutoriales/<slug>/', views.tutorialDetallado,
        name='tutorial-detallado'),
    path('leyes/', views.leyesView, name='leyes'),
    path('success/', views.SuccessView.as_view()), # new
    path('cancelled/', views.CancelledView.as_view()), # new
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 