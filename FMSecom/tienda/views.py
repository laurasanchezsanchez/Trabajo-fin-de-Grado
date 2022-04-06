from django.shortcuts import render
from .models import Categorias_productos
from .models import Productos

from ecommerce.models import Informacion_index
from ecommerce.models import Informacion_empresa
from ecommerce.models import Informacion_instalaciones
from ecommerce.models import Empresas_apoyo

#añadido para cambiar de vistas
from dataclasses import fields
from pdb import post_mortem
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.views import generic

# Create your views here.

# ------------------------------------------------------------------------
# Esta funcion nos devuelve todas las categorias 
# ------------------------------------------------------------------------

def categorias(request):
    return render(request, "tienda/categorias.html",
    {
    "telefono" :Informacion_empresa.objects.get(identificador="Numero de telefono"),
    "email" : Informacion_empresa.objects.get(identificador="Email"),
    "ubicacion": Informacion_empresa.objects.get(identificador="Ubicacion"),
    
    "categorias" : Categorias_productos.objects.all
    } )


# ------------------------------------------------------------------------
# Esta funcion nos devuelve todos los productos de una categoria concreta
# ------------------------------------------------------------------------

def categoria_filtrada(request, slug_categoria):
    return render(request, "tienda/categoria_filtrada.html",
    {
    "telefono" :Informacion_empresa.objects.get(identificador="Numero de telefono"),
    "email" : Informacion_empresa.objects.get(identificador="Email"),
    "ubicacion": Informacion_empresa.objects.get(identificador="Ubicacion"),

    "Empresas_apoyo" : Empresas_apoyo.objects.all,
    "categoria" : Categorias_productos.objects.get(slug=slug_categoria),
    "productos" : Productos.objects.filter(categoria_slug=slug_categoria)
    } )



def producto_detallado(request, slug_categoria, slug_producto):
    return render(request, "tienda/producto_detallado.html",
    {
    "telefono" :Informacion_empresa.objects.get(identificador="Numero de telefono"),
    "email" : Informacion_empresa.objects.get(identificador="Email"),
    "ubicacion": Informacion_empresa.objects.get(identificador="Ubicacion"),

    "categoria" : Categorias_productos.objects.get(slug=slug_categoria),
    "productos_categoria" : Productos.objects.filter(categoria_slug=slug_categoria).exclude(nombre_slug=slug_producto),
    "producto" : Productos.objects.filter(nombre_slug=slug_producto).first
    } )


    
# ------------------------------------------------------------------------
#
# ------------------------------------------------------------------------
