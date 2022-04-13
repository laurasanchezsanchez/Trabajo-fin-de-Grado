from django.contrib import admin

# Register your models here.

from .models import Categorias_productos, Productos, Pedido, ItemPedido

class categoriasAdministrador(admin.ModelAdmin):
    # Orden en el que se muestran
    list_display = ('nombre_categoria', 'slug')     
    # Campo filtrado
    list_filter = ("nombre_categoria",)          
    # Campo de búsqueda                              
    search_fields = ['nombre_categoria', ]                 
    exclude = ('slug',)  
    readonly_fields = ('fecha_creacion', 'ultima_modificacion')

class productosAdministrador(admin.ModelAdmin):
    # Orden en el que se muestran
    list_display = ('categoria', 'categoria_slug', 'nombre', 'slug', 'precio_producto', 'precio_producto_servicio', 'tipo', 'id')     
    # Campo filtrado
    list_filter = ("categoria", "nombre",)  
    # Campo de búsqueda                                      
    search_fields = ['categoria', 'nombre', ]                            
    exclude = ('categoria_slug', 'slug', )  



admin.site.register(Categorias_productos, categoriasAdministrador)
admin.site.register(Productos, productosAdministrador)

admin.site.register(Pedido)
admin.site.register(ItemPedido)
