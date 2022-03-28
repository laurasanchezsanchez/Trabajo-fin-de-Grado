from django.db import models

# Create your models here.
class Camara(models.Model):
    nombre_camara = models.CharField(max_length=200)
    fecha_publicacion_camara = models.DateTimeField('date published')
    descripcion_camara = models.CharField(max_length=500)

    def __str__(self):
        return self.nombre_camara

        

class informacion_index(models.Model):
    identificador = models.CharField(max_length=1000)
    titulo_informacion = models.CharField(max_length=1000, null=True, blank=True)
    descripcion_informacion = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.identificador


class informacion_empresa(models.Model):
    identificador = models.CharField(max_length=1000)
    titulo_informacion = models.CharField(max_length=1000, null=True, blank=True)
    dato_1 = models.CharField(max_length=10000, null=True, blank=True)
    dato_2 = models.CharField(max_length=10000, null=True, blank=True)

    def __str__(self):
        return self.identificador

class informacion_instalaciones(models.Model):
    identificador = models.CharField(max_length=1000)
    titulo_informacion = models.CharField(max_length=500, null=True, blank=True)
    descripcion_informacion = models.CharField(max_length=10000, null=True, blank=True)

    def __str__(self):
        return self.identificador