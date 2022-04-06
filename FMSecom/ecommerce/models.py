from django.db import models

#añadidos - recortar
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date

import string, random
from django.dispatch import receiver
from django.db.models.signals import pre_save

    
class Informacion_index(models.Model):
    identificador = models.CharField(max_length=1000)
    titulo_informacion = models.CharField(max_length=1000, null=True, blank=True)
    descripcion_informacion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.identificador


class Informacion_empresa(models.Model):
    identificador = models.CharField(max_length=1000)
    titulo_informacion = models.CharField(max_length=1000, null=True, blank=True)
    dato_1 = models.TextField(null=True, blank=True)
    dato_2 = models.TextField(null=True, blank=True)
    imagen = models.ImageField(null=True, blank=True, upload_to="images/")
    
    def __str__(self):
        return self.identificador

class Empresas_apoyo(models.Model):
    identificador = models.CharField(max_length=1000)
    imagen = models.ImageField(null=True, blank=True, upload_to="images/")
    
    def __str__(self):
        return self.identificador

class Informacion_instalaciones(models.Model):
    identificador = models.CharField(max_length=1000)
    titulo_informacion = models.CharField(max_length=500, null=True, blank=True)
    descripcion_informacion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.identificador