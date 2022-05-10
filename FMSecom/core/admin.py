from django.contrib import admin

# Register your models here.

from .models import Informacion_index
from .models import Informacion_empresa
from .models import Informacion_instalaciones
from .models import Empresas_apoyo
from .models import Manuales



admin.site.register(Informacion_index)
admin.site.register(Informacion_empresa)
admin.site.register(Informacion_instalaciones)
admin.site.register(Empresas_apoyo)
admin.site.register(Manuales)


