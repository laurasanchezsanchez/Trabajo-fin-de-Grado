from turtle import Turtle
from django.contrib import admin

# Register your models here.

from .models import Informacion_index
from .models import Informacion_empresa
from .models import Informacion_instalaciones
from .models import Empresas_apoyo
from .models import Manuales
from .models import Tutoriales
from .models import Leyes

class tutorialesAdministrador(admin.ModelAdmin):            
    exclude = ('slug',) 

class leyesAdmin(admin.ModelAdmin):
    list_display = [
        'titulo'
    ]
    list_filter = ("titulo",) 

class manualesAdmin(admin.ModelAdmin):
    list_display = [
        'titulo',
        'categoria'
    ]
    list_filter = ("categoria", "titulo",) 


admin.site.register(Empresas_apoyo)
admin.site.register(Manuales, manualesAdmin)
admin.site.register(Tutoriales, tutorialesAdministrador)
admin.site.register(Leyes, leyesAdmin)


class readonlyAdministrador(admin.ModelAdmin):
    readonly_fields = ('identificador',)


admin.site.register(Informacion_index, readonlyAdministrador)
admin.site.register(Informacion_empresa, readonlyAdministrador)
admin.site.register(Informacion_instalaciones, readonlyAdministrador)


