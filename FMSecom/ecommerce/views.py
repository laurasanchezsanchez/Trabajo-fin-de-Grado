from django.shortcuts import render
from django.views import generic
# Create your views here.
from django.http import HttpResponse
from django.template import loader


from .models import Informacion_index
from .models import Informacion_empresa
from .models import Informacion_instalaciones
from .models import Empresas_apoyo

import importlib.util

#necesita importar las categorias
from tienda.models import Categorias_productos
from tienda.models import Productos
#añadido para cambiar de vistas
from dataclasses import fields
from pdb import post_mortem
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404

#prueba
from wsgiref.util import FileWrapper


class indexListView(generic.ListView):
    model = Categorias_productos
    template_name = 'ecommerce/index.html'

    def get_context_data(self, **kwargs):
        context = super(indexListView, self).get_context_data(**kwargs)
        context['acerca_de'] = Informacion_index.objects.get(identificador="Acerca de")
        context['slider_1'] = Informacion_index.objects.get(identificador="Slider 1")
        context['slider_2'] = Informacion_index.objects.get(identificador="Slider 2")
        context['slider_3'] = Informacion_index.objects.get(identificador="Slider 3")
        context['descripcion_del_personal'] = Informacion_index.objects.get(identificador="Descripcion del personal")
        context['descripcion_de_servicios'] = Informacion_index.objects.get(identificador="Descripcion de servicios")
        context['titulo_de_oferta'] = Informacion_index.objects.get(identificador="Titulo de oferta")
        context['datos_obligatorios'] = Informacion_index.objects.get(identificador="Datos obligatorios")
        context['telefono'] = Informacion_empresa.objects.get(identificador="Numero de telefono")
        context['email'] = Informacion_empresa.objects.get(identificador="Email")
        context['ubicacion'] = Informacion_empresa.objects.get(identificador="Ubicacion")
        context['imagen_camara_publicitaria'] = Informacion_empresa.objects.get(identificador="Imagen camara publicitaria")
        context['Empresas_apoyo'] = Empresas_apoyo.objects.all
        return context

# ------------------------------------------------------------------------
#
# ------------------------------------------------------------------------


def ofertas(request):
    
    telefono = Informacion_empresa.objects.get(identificador="Numero de telefono")
    email = Informacion_empresa.objects.get(identificador="Email")
    ubicacion = Informacion_empresa.objects.get(identificador="Ubicacion")

    return render(request, 'ecommerce/ofertas.html', 
    {'telefono' : telefono,
    'email' : email,
    'ubicacion' : ubicacion
    })



def tutoriales(request):
    telefono = Informacion_empresa.objects.get(identificador="Numero de telefono")
    email = Informacion_empresa.objects.get(identificador="Email")
    ubicacion = Informacion_empresa.objects.get(identificador="Ubicacion")

    return render(request, 'ecommerce/tutoriales.html', 
    {'telefono' : telefono,
    'email' : email,
    'ubicacion' : ubicacion
    })

def contacto(request):
    telefono = Informacion_empresa.objects.get(identificador="Numero de telefono")
    email = Informacion_empresa.objects.get(identificador="Email")
    ubicacion = Informacion_empresa.objects.get(identificador="Ubicacion")
    redes_sociales = Informacion_empresa.objects.get(identificador="Redes sociales")

    return render(request, 'ecommerce/contacto.html', 
    {'telefono' : telefono,
    'email' : email,
    'ubicacion' : ubicacion,
    'redes_sociales' : redes_sociales
    })

def instalaciones(request):
    telefono = Informacion_empresa.objects.get(identificador="Numero de telefono")
    email = Informacion_empresa.objects.get(identificador="Email")
    ubicacion = Informacion_empresa.objects.get(identificador="Ubicacion")
    redes_sociales = Informacion_empresa.objects.get(identificador="Redes sociales")
    paso_1 = Informacion_instalaciones.objects.get(identificador="Paso 1")
    paso_2 = Informacion_instalaciones.objects.get(identificador="Paso 2")
    paso_3 = Informacion_instalaciones.objects.get(identificador="Paso 3")


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
    telefono = Informacion_empresa.objects.get(identificador="Numero de telefono")
    email = Informacion_empresa.objects.get(identificador="Email")
    ubicacion = Informacion_empresa.objects.get(identificador="Ubicacion")
    redes_sociales = Informacion_empresa.objects.get(identificador="Redes sociales")
    paso_1 = Informacion_instalaciones.objects.get(identificador="Paso 1")
    paso_2 = Informacion_instalaciones.objects.get(identificador="Paso 2")
    paso_3 = Informacion_instalaciones.objects.get(identificador="Paso 3")
    receptora = Informacion_empresa.objects.get(identificador="Servicio receptora")


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



