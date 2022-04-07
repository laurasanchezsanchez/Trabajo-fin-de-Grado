from django.urls import path

from .views import VistaRegistro, cerrar_sesion, loguear

app_name = 'autenticacion'

#arreglar barra tutoriales
urlpatterns = [
    path('', VistaRegistro.as_view(), name='autenticacion'),
    path('cerrar_sesion', cerrar_sesion, name='cerrar_sesion'),
    path('login', loguear, name='login')
]