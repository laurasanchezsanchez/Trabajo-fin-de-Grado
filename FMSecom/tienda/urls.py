from django.urls import path

from . import views
from . views import categorias
from django.template.defaultfilters import slugify


app_name = 'tienda'

#arreglar barra tutoriales
urlpatterns = [
    path('', views.categorias, name='categorias'),
    path('categoria/<slug:slug_categoria>/',views.categoria_filtrada, name='categoria'),
    path('categoria/<slug:slug_categoria>/<slug:slug_producto>/',views.producto_detallado, name='producto'),

]