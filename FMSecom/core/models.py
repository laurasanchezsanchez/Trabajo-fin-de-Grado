from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import pre_save
from numpy import deg2rad
from tienda.models import Categorias_productos
from ckeditor.fields import RichTextField
from django.template.defaultfilters import slugify

    
class Informacion_index(models.Model):
    identificador = models.CharField(max_length=1000)
    titulo_informacion = models.CharField(max_length=1000, null=True, blank=True)
    descripcion_informacion = RichTextField(null=True, blank=True)

    def __str__(self):
        return self.identificador


class Informacion_empresa(models.Model):
    identificador = models.CharField(max_length=1000)
    titulo_informacion = models.CharField(max_length=1000, null=True, blank=True)
    dato_1 = RichTextField(null=True, blank=True)
    dato_2 = RichTextField(null=True, blank=True)
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
    descripcion_informacion = RichTextField(null=True, blank=True)

    def __str__(self):
        return self.identificador


class Manuales(models.Model):
    titulo = models.CharField(max_length = 200)
    archivo = models.FileField(upload_to = "pdfs/manuales/")

    categoria = models.ForeignKey(
        Categorias_productos, on_delete=models.CASCADE)

class Tutoriales(models.Model):
    titulo = models.CharField(max_length=1000)
    slug = models.SlugField(max_length=500, unique=True, null=True, blank=True)
    descripcion = RichTextField(null=True, blank=True)

    paso_1 = models.CharField(max_length=1000)
    descripcion_paso_1 = RichTextField(null=True, blank=True)
    url_descarga = models.CharField(max_length=2000, null=True, blank=True)
    imagen_paso_1 = models.ImageField(null=True, blank=True, upload_to="images/tutoriales")

    paso_2 = models.CharField(max_length=1000)
    descripcion_paso_2 = RichTextField(max_length=2000, null=True, blank=True)
    imagen_paso_2 = models.ImageField(null=True, blank=True, upload_to="images/tutoriales")

    paso_3 = models.CharField(max_length=1000)
    descripcion_paso_3 = RichTextField(max_length=2000, null=True, blank=True)
    imagen_paso_3 = models.ImageField(null=True, blank=True, upload_to="images/tutoriales")

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        self.slug = slugify(self.titulo)
        super(Tutoriales, self).save(*args, **kwargs)



class Leyes(models.Model):
    titulo = models.CharField(max_length = 200)
    archivo = models.FileField(upload_to = "pdfs/leyes/")
