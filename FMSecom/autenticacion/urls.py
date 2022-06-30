from django.urls import path

from .views import VistaRegistro, cerrar_sesion, loguear, perfilView, password_success

app_name = 'autenticacion'

#arreglar barra tutoriales
urlpatterns = [
    path('', VistaRegistro.as_view(), name='autenticacion'),
    path('cerrar_sesion', cerrar_sesion, name='cerrar_sesion'),
    path('login', loguear, name='login'),
    path('perfil', perfilView.as_view(), name='perfil'),
    path('password_success', password_success, name="password_success"),
]