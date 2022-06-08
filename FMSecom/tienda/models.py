from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.shortcuts import reverse
from ckeditor.fields import RichTextField

User = get_user_model()

# ------------------------------------------------------------------------
# Tabla de las categorias (Alarmas, Camaras, Grabadores...)
# ------------------------------------------------------------------------


class Categorias_productos(models.Model):
    nombre_categoria = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=500, unique=True, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre_categoria

    # Metodo que nos devuelve la url de los detalles del producto
    def get_absolute_url(self):
        return reverse('tienda:categoria-detallada', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nombre_categoria)
        super(Categorias_productos, self).save(*args, **kwargs)


# ------------------------------------------------------------------------
# Tabla de los productos. Tendrán foreign key a la categoria correspondiente
# ------------------------------------------------------------------------

class Productos(models.Model):
    categoria = models.ForeignKey(
        Categorias_productos, on_delete=models.CASCADE)
    categoria_slug = models.SlugField(max_length=500, null=True, blank=True)
    nombre = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=500, unique=True, null=True, blank=True)
    imagen1 = models.ImageField(upload_to="images/productos", null=True,
                                blank=True, default="images/productos/Camara1_lzyN5KJ.png")
    imagen2 = models.ImageField(
        null=True, blank=True, upload_to="images/productos")
    imagen3 = models.ImageField(
        null=True, blank=True, upload_to="images/productos")
    descripcion = RichTextField(null=True, blank=True)
    especificaciones = RichTextField(null=True, blank=True)
    precio_producto = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return str(self.categoria) + '          |           ' + str(self.nombre)

    def save(self, *args, **kwargs):
        self.categoria_slug = slugify(self.categoria)
        self.slug = slugify(self.nombre)
        
        super(Productos, self).save(*args, **kwargs)

    # Metodo que nos devuelve la url de los detalles del producto
    def get_absolute_url(self):
        return reverse('tienda:producto-detallado', kwargs={'slug': self.slug})

# ------------------------------------------------------------------------
# Tabla para filtrar productos segun nombre, descripcion o especificaciones.
# ------------------------------------------------------------------------




# ------------------------------------------------------------------------
# Tabla de los pedidos. Pueden estar o no realizados.
# ------------------------------------------------------------------------

class Pedido(models.Model):
    # Como un user no registrado puede tambien agregar al carrito, ponemos blank y null
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    fecha = models.DateTimeField(blank=True, null=True)
    realizado = models.BooleanField(default=False)

    # Si una direccion se borra no se debe borrar el pedido
    direccion_facturacion = models.ForeignKey(
        "Direccion", related_name='direccion_facturacion', blank=True, null=True, on_delete=models.SET_NULL)
    direccion_envio = models.ForeignKey(
        "Direccion", related_name='direccion_envio', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.reference_number

    @property
    def reference_number(self):
        return f"PEDIDO - {self.pk}"

    # Devuelve el total DEL PEDIDO
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += float(order_item.precio_producto_cantidad())
        return total



# ------------------------------------------------------------------------
# Clase que esta entre el carrito y el producto
# ------------------------------------------------------------------------

class ItemPedido(models.Model):
    pedido = models.ForeignKey(
        Pedido, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)

    # La cantidad no nos hará falta por ahora
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.reference_number

    @property
    def reference_number(self):
        return f"{self.cantidad}    x   {self.producto.nombre}"
        

    # Precio en centimos del producto * su cantidad
    def precio_producto_cantidad(self):
        return self.cantidad * self.producto.precio_producto




# ------------------------------------------------------------------------
# Clase que guarda las direcciones de envio y facturacion. El usuario debe estar registrado.
# ------------------------------------------------------------------------

class Direccion(models.Model):
    direccion_CHOICES = (
        ('F', 'Facturacion'),
        ('E', 'Envio'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    direccion_1 = models.CharField(max_length=150)
    direccion_2 = models.CharField(max_length=150)
    ciudad = models.CharField(max_length=100)
    codigo_zip = models.CharField(max_length=100)
    direccion_tipo = models.CharField(max_length=1, choices=direccion_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.direccion_1}, {self.direccion_2}, {self.ciudad}, {self.codigo_zip} "

    class Meta:
        verbose_name_plural = 'direcciones'


# ------------------------------------------------------------------------
# Clase que guarda la informacion sobre los pagos, métodos de pago, fecha, importe...
# ------------------------------------------------------------------------

class Pago(models.Model):
    pedido = models.ForeignKey(
        Pedido, on_delete=models.CASCADE, related_name='payments')
    metodo_pago = models.CharField(max_length=20, choices=(
        ('Paypal', 'Paypal'),
    ))
    fecha = models.DateTimeField(auto_now_add=True)
    succesful = models.BooleanField(default=False)
    importe = models.DecimalField(max_digits=12, decimal_places=2)

    # Respuesta del procesador de pago
    respuesta_pasarela_pago = models.TextField()

    def __str__(self):
        return self.reference_number

    @property
    def reference_number(self):
        return f"PAGO-{self.pedido}-{self.pk}"


