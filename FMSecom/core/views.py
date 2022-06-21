from django.shortcuts import render
from django.views import generic
# Create your views here.
from django.http import HttpResponse
from django.template import loader


from .models import Informacion_index, Tutoriales
from .models import Informacion_empresa
from .models import Informacion_instalaciones
from .models import Empresas_apoyo
from .models import Manuales
from .models import Leyes
from django.views.generic.base import TemplateView
import importlib.util

# necesita importar las categorias
from tienda.models import Categorias_productos
from tienda.models import Productos
# añadido para cambiar de vistas
from dataclasses import fields
from pdb import post_mortem
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404

# prueba
from wsgiref.util import FileWrapper
from .forms import ContactForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, reverse
from django.urls import reverse_lazy


def baseView(request):
    productos = Productos.objects.all()

    return render(request, 'core/base.html',
                  {
                      'productos': productos,
                  })


class indexListView(generic.ListView):
    model = Categorias_productos
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super(indexListView, self).get_context_data(**kwargs)
        context['acerca_de'] = Informacion_index.objects.get(
            identificador="Acerca de")
        context['slider_1'] = Informacion_index.objects.get(
            identificador="Slider 1")
        context['slider_2'] = Informacion_index.objects.get(
            identificador="Slider 2")
        context['slider_3'] = Informacion_index.objects.get(
            identificador="Slider 3")
        context['descripcion_del_personal'] = Informacion_index.objects.get(
            identificador="Descripcion del personal")
        context['descripcion_de_servicios'] = Informacion_index.objects.get(
            identificador="Descripcion de servicios")
        context['datos_obligatorios'] = Informacion_index.objects.get(
            identificador="Datos obligatorios")

        context['imagen_camara_publicitaria'] = Informacion_empresa.objects.get(
            identificador="Imagen camara publicitaria")
        context['Empresas_apoyo'] = Empresas_apoyo.objects.all
        return context

# ------------------------------------------------------------------------
#
# ------------------------------------------------------------------------



def tutoriales(request):

    tutoriales = Tutoriales.objects.all()

    return render(request, 'core/tutoriales.html',{
                      'tutoriales': tutoriales
                  })

def tutorialDetallado(request, slug):
    return render(request, "core/tutorial_detallado.html",
                  {
                      "tutorial": Tutoriales.objects.filter(slug=slug).first(),
                  })


def instalaciones(request):
    redes_sociales = Informacion_empresa.objects.get(
        identificador="Redes sociales")
    paso_1 = Informacion_instalaciones.objects.get(identificador="Paso 1")
    paso_2 = Informacion_instalaciones.objects.get(identificador="Paso 2")
    paso_3 = Informacion_instalaciones.objects.get(identificador="Paso 3")

    return render(request, 'core/instalaciones.html',
                  {
                      'redes_sociales': redes_sociales,
                      'paso_1': paso_1,
                      'paso_2': paso_2,
                      'paso_3': paso_3
                  })


def receptora(request):
    redes_sociales = Informacion_empresa.objects.get(
        identificador="Redes sociales")
    paso_1 = Informacion_instalaciones.objects.get(identificador="Paso 1")
    paso_2 = Informacion_instalaciones.objects.get(identificador="Paso 2")
    paso_3 = Informacion_instalaciones.objects.get(identificador="Paso 3")
    receptora = Informacion_empresa.objects.get(
        identificador="Servicio receptora")

    return render(request, 'core/receptora.html',
                  {
                      'redes_sociales': redes_sociales,
                      'paso_1': paso_1,
                      'paso_2': paso_2,
                      'paso_3': paso_3,
                      'receptora': receptora
                  })


def contacto(request):
    redes_sociales = Informacion_empresa.objects.get(
        identificador="Redes sociales")

    return render(request, 'core/contacto.html',
                  {
                      'redes_sociales': redes_sociales
                  })

# Para que un cliente nos pueda mandar un mensaje a traves de la web


class ContactView(generic.FormView):
    form_class = ContactForm
    template_name = 'core/contacto.html'

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)
        context['redes_sociales'] = Informacion_empresa.objects.get(
            identificador="Redes sociales")

        return context

    def get_success_url(self):
        return reverse('core:contacto')

    def form_valid(self, form):
        messages.info(
            self.request, "Gracias por su mensaje. Lo hemos recibido correctamente.")

        nombre = form.cleaned_data.get('nombre')
        email = form.cleaned_data.get('email')
        mensaje = form.cleaned_data.get('mensaje')

        full_message = f"""
            Mensaje recibibo de {nombre}, con el correo electronico: {email}
            ___________________________________
            Mensaje:


            {mensaje}
            """
        form.send()
        form.send_confirmation()
        return super(ContactView, self).form_valid(form)


def manualesView(request):
    
    documents = Manuales.objects.all()
    categorias = Categorias_productos.objects.all()

    return render(request, "core/manuales.html", context = {
        "files": documents,
        "categorias" : categorias,
    })


def leyesView(request):
    
    documents = Leyes.objects.all()

    return render(request, "core/leyes.html", context = {
        "files": documents,
    })

class SuccessView(TemplateView):
    template_name = 'core/success.html'


class CancelledView(TemplateView):
    template_name = 'core/cancelled.html'