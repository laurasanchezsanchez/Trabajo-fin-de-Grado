from django.contrib import admin

# Register your models here.

from .models import informacion_index
from .models import informacion_empresa
from .models import informacion_instalaciones
from .models import otras_empresas

admin.site.register(informacion_index)
admin.site.register(informacion_empresa)
admin.site.register(informacion_instalaciones)
admin.site.register(otras_empresas)