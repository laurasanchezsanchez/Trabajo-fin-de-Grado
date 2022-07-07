from django.contrib import admin

# Register your models here.

from .models import Categorias_productos, Productos, Pedido, ItemPedido, Direccion

class categoriasAdministrador(admin.ModelAdmin):
    # Orden en el que se muestran
    list_display = ('nombre_categoria',)     
    # Campo filtrado
    list_filter = ("nombre_categoria",)          
    # Campo de búsqueda                                    
    exclude = ('slug',)  
    readonly_fields = ('fecha_creacion', 'ultima_modificacion')

class productosAdministrador(admin.ModelAdmin):
    # Orden en el que se muestran
    list_display = ('categoria', 'nombre', 'precio_producto', 'id')     
    # Campo filtrado
    list_filter = ("categoria", "nombre",)  
    # Campo de búsqueda                                                 
    exclude = ('categoria_slug', 'slug', )  
    list_editable = ['precio_producto']
    list_per_page = 10

class direccionAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'direccion_1',
        'direccion_2',
        'codigo_zip',
        'ciudad',
        'direccion_tipo',
        
    ]
    fields = ['user', ('direccion_1', 'direccion_2'), ('ciudad', 'codigo_zip'), 'direccion_tipo']


class pedidoAdmin(admin.ModelAdmin):
    list_display = [
        'reference_number',
        'user',
        'start_date',
        'direccion_facturacion',
        'direccion_envio',
        'get_total',
        'realizado',
        'fecha'
    ]

class itemPedidoAdmin(admin.ModelAdmin):
    list_display = [
        'pedido',
        'producto',
        'cantidad',
        'precio_producto_cantidad',
    ]

    



admin.site.register(Categorias_productos, categoriasAdministrador)
admin.site.register(Productos, productosAdministrador)

admin.site.register(Pedido, pedidoAdmin)
admin.site.register(ItemPedido, itemPedidoAdmin)
admin.site.register(Direccion, direccionAdmin)

