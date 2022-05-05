
from core.models import Informacion_empresa
from core.models import Empresas_apoyo


def subject_renderer(request):
    return {
        'email': Informacion_empresa.objects.get(identificador="Email"),
        'ubicacion': Informacion_empresa.objects.get(identificador="Ubicacion"),
        'telefono': Informacion_empresa.objects.get(identificador="Numero de telefono"),
        'Empresas_apoyo': Empresas_apoyo.objects.all,

    }
