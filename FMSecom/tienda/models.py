from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.


# ------------------------------------------------------------------------
# Tabla de las categorias (Alarmas, Camaras, Grabadores...)
# ------------------------------------------------------------------------
class Categorias_productos(models.Model):
    nombre_categoria = models.CharField(max_length=200, unique=True)
    slug= models.SlugField(max_length=500, unique=True, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_modificacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre_categoria

    # Metodo que nos devuelve la url de los detalles del producto
    def get_absolute_url(self):
        return reverse('categoria-detallada', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre_categoria)
        super(Categorias_productos, self).save(*args, **kwargs)



# ------------------------------------------------------------------------
# Tabla de los productos. Tendrán foreign key a la categoria correspondiente
# ------------------------------------------------------------------------
class Productos(models.Model):
    categoria = models.ForeignKey(Categorias_productos, on_delete=models.CASCADE)
    categoria_slug= models.SlugField(max_length=500, null=True, blank=True)
    nombre = models.CharField(max_length=200, unique=True)
    nombre_slug= models.SlugField(max_length=500, unique=True, null=True, blank=True)
    # Probar a cambiar poniendo: upload_to='productos' 
    imagen1 = models.ImageField(upload_to="images/productos", null=True, blank=True, default="images/productos/Camara1_lzyN5KJ.png")
    imagen2 = models.ImageField(null=True, blank=True, upload_to="images/productos")
    imagen3 = models.ImageField(null=True, blank=True, upload_to="images/productos")
    imagen4 = models.ImageField(null=True, blank=True, upload_to="images/productos")
    descripcion = models.TextField(null=True, blank=True)
    especificaciones = models.TextField(null=True, blank=True)
    precio_producto = models.PositiveIntegerField()
    precio_producto_servicio = models.PositiveIntegerField()
    tipo = models.CharField(max_length=200, default = "Sin tipo")

    def __str__(self):
        return str(self.categoria) + '          |           ' + str(self.nombre) 
    #+ ' | ' + str(self.tipo)

    # Metodo que nos devuelve la url de los detalles del producto
    def get_absolute_url(self):
        return reverse('producto-detallado', kwargs={'nombre_slug': self.nombre_slug})

    def save(self, *args, **kwargs):
        self.categoria_slug = slugify(self.categoria)
        self.nombre_slug = slugify(self.nombre)
        super(Productos, self).save(*args, **kwargs)
