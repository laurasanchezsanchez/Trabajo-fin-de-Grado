from django.contrib import admin

# Register your models here.

from .models import Categorias_productos, Productos, Pedido, ItemPedido, Direccion

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
    list_display = ('categoria', 'categoria_slug', 'nombre', 'slug', 'precio_producto', 'id')     
    # Campo filtrado
    list_filter = ("categoria", "nombre",)  
    # Campo de búsqueda                                      
    search_fields = ['categoria', 'nombre', ]                            
    exclude = ('categoria_slug', 'slug', )  

class direccionAdmin(admin.ModelAdmin):
    list_display = [
        'direccion_1',
        'direccion_2',
        'codigo_zip',
        'ciudad',
        'direccion_tipo'
    ]

class ItemInline(admin.TabularInline):
    model = ItemPedido
    fk_name = "pedido"

class pedidoAdmin(admin.ModelAdmin):
    list_display = [
        'reference_number',
        'user',
        'start_date',
        'direccion_facturacion',
        'direccion_envio',
        'get_total',
        'realizado',
        'get_items'
    ]

    def get_items(self, obj):
        return obj.get_items.pedido


admin.site.register(Categorias_productos, categoriasAdministrador)
admin.site.register(Productos, productosAdministrador)

admin.site.register(Pedido, pedidoAdmin)
admin.site.register(ItemPedido)
admin.site.register(Direccion, direccionAdmin)
