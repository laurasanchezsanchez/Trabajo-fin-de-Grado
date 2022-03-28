from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

from .models import Camara
from .models import informacion_index
from .models import informacion_empresa
from .models import informacion_instalaciones


#prueba
from wsgiref.util import FileWrapper

def index(request):
    acerca_de = informacion_index.objects.get(identificador="Acerca de")
    slider_1 = informacion_index.objects.get(identificador="Slider 1")
    slider_2 = informacion_index.objects.get(identificador="Slider 2")
    slider_3 = informacion_index.objects.get(identificador="Slider 3")
    descripcion_del_personal = informacion_index.objects.get(identificador="Descripcion del personal")
    descripcion_de_servicios = informacion_index.objects.get(identificador="Descripcion de servicios")
    titulo_de_oferta = informacion_index.objects.get(identificador="Titulo de oferta")
    datos_obligatorios = informacion_index.objects.get(identificador="Datos obligatorios")
    telefono = informacion_empresa.objects.get(identificador="Numero de telefono")
    email = informacion_empresa.objects.get(identificador="Email")
    ubicacion = informacion_empresa.objects.get(identificador="Ubicacion")


    return render(request, 'ecommerce/index.html', 
    {'acerca_de': acerca_de, 
    'slider_1': slider_1,  
    'slider_2': slider_2, 
    'slider_3' : slider_3, 
    'descripcion_del_personal' : descripcion_del_personal, 
    'descripcion_de_servicios' : descripcion_de_servicios, 
    'titulo_de_oferta' : titulo_de_oferta,
    'datos_obligatorios' : datos_obligatorios,
    'telefono' : telefono,
    'email' : email,
    'ubicacion' : ubicacion
    })

def ofertas(request):
    return render(request, 'ecommerce/ofertas.html' )

#arreglar
def tutoriales(request):
    telefono = informacion_empresa.objects.get(identificador="Numero de telefono")
    email = informacion_empresa.objects.get(identificador="Email")
    ubicacion = informacion_empresa.objects.get(identificador="Ubicacion")


    return render(request, 'ecommerce/tutoriales.html', 
    {'telefono' : telefono,
    'email' : email,
    'ubicacion' : ubicacion
    })

def contacto(request):
    telefono = informacion_empresa.objects.get(identificador="Numero de telefono")
    email = informacion_empresa.objects.get(identificador="Email")
    ubicacion = informacion_empresa.objects.get(identificador="Ubicacion")
    redes_sociales = informacion_empresa.objects.get(identificador="Redes sociales")


    return render(request, 'ecommerce/contacto.html', 
    {'telefono' : telefono,
    'email' : email,
    'ubicacion' : ubicacion,
    'redes_sociales' : redes_sociales
    })

def instalaciones(request):
    telefono = informacion_empresa.objects.get(identificador="Numero de telefono")
    email = informacion_empresa.objects.get(identificador="Email")
    ubicacion = informacion_empresa.objects.get(identificador="Ubicacion")
    redes_sociales = informacion_empresa.objects.get(identificador="Redes sociales")
    paso_1 = informacion_instalaciones.objects.get(identificador="Paso 1")
    paso_2 = informacion_instalaciones.objects.get(identificador="Paso 2")
    paso_3 = informacion_instalaciones.objects.get(identificador="Paso 3")


    return render(request, 'ecommerce/instalaciones.html', 
    {'telefono' : telefono,
    'email' : email,
    'ubicacion' : ubicacion,
    'redes_sociales' : redes_sociales,
    'paso_1' : paso_1,
    'paso_2' : paso_2,
    'paso_3' : paso_3
    })

def receptora(request):
    telefono = informacion_empresa.objects.get(identificador="Numero de telefono")
    email = informacion_empresa.objects.get(identificador="Email")
    ubicacion = informacion_empresa.objects.get(identificador="Ubicacion")
    redes_sociales = informacion_empresa.objects.get(identificador="Redes sociales")
    paso_1 = informacion_instalaciones.objects.get(identificador="Paso 1")
    paso_2 = informacion_instalaciones.objects.get(identificador="Paso 2")
    paso_3 = informacion_instalaciones.objects.get(identificador="Paso 3")
    receptora = informacion_empresa.objects.get(identificador="Servicio receptora")


    return render(request, 'ecommerce/receptora.html', 
    {'telefono' : telefono,
    'email' : email,
    'ubicacion' : ubicacion,
    'redes_sociales' : redes_sociales,
    'paso_1' : paso_1,
    'paso_2' : paso_2,
    'paso_3' : paso_3,
    'receptora' : receptora
    })

