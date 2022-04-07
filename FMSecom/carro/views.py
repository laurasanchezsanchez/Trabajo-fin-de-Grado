from django.shortcuts import render

from .carro import Carro
from tienda.models import Productos
from tienda.models import Categorias_productos 
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import HttpResponseRedirect
# Create your views here.


def agregar_producto(request, producto_id):
    carro=Carro(request)
    producto=Productos.objects.get(id=producto_id)
    carro.agregar(producto=producto)
    return HttpResponseRedirect(reverse('tienda:producto', args=(producto.categoria_slug, producto.nombre_slug)))


def eliminar_producto(request, producto_id):
    carro=Carro(request)
    producto=Productos.objects.get(id=producto_id)
    carro.eliminar(producto=producto)

    return HttpResponseRedirect(reverse('tienda:producto', args=(producto.categoria_slug, producto.nombre_slug)))


def restar_producto(request, producto_id):
    carro=Carro(request)
    producto=Productos.objects.get(id=producto_id)
    carro.restar_producto(producto=producto)

    return HttpResponseRedirect(reverse('tienda:producto', args=(producto.categoria_slug, producto.nombre_slug)))


def limpiar_carro(request, producto_id):
    carro=Carro(request)
    carro.limpiar_carro()
    producto=Productos.objects.get(id=producto_id)

    return HttpResponseRedirect(reverse('tienda:producto', args=(producto.categoria_slug, producto.nombre_slug)))