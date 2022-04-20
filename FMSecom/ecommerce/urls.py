from django.urls import path

from . import views

from . views import indexListView
from . views import ContactView


app_name = 'ecommerce'

#arreglar barra tutoriales
urlpatterns = [
    path('', indexListView.as_view(), name='index'),
    path('ofertas/', views.ofertas, name='ofertas'),
    path('tutoriales', views.tutoriales, name='tutoriales'),
    path('instalaciones/', views.instalaciones, name='instalaciones'),
    path('receptora', views.receptora, name='receptora'),
    path('contacto/', views.ContactView.as_view(), name='contacto'),
]