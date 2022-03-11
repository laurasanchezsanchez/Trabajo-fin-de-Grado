from django.db import models

# Create your models here.
class Camara(models.Model):
    nombre_camara = models.CharField(max_length=200)
    fecha_publicacion_camara = models.DateTimeField('date published')
    descripcion_camara = models.CharField(max_length=500)

    def __str__(self):
        return self.nombre_camara