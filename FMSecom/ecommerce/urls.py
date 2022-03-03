from django.urls import path

from . import views

app_name = 'fmsecom'

urlpatterns = [
    path('', views.index, name='index'),
]