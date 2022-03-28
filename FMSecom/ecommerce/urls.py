from django.urls import path

from . import views

app_name = 'fmsecom'

urlpatterns = [
    path('', views.index, name='index'),
    path('ofertas/', views.ofertas, name='ofertas'),
    path('tutoriales/', views.tutoriales, name='tutoriales'),
    path('contacto/', views.contacto, name='contacto'),
    path('instalaciones/', views.instalaciones, name='instalaciones'),
    path('receptora/', views.receptora, name='receptora'),
]