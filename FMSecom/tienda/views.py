from django.shortcuts import render
from .models import Categorias_productos, ItemPedido
from .models import Productos

from ecommerce.models import Informacion_index
from ecommerce.models import Informacion_empresa
from ecommerce.models import Informacion_instalaciones
from ecommerce.models import Empresas_apoyo

# añadido para cambiar de vistas
from dataclasses import fields
from pdb import post_mortem
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, reverse, redirect
from django.views import generic
from .forms import AnadirAlCarrito
from .utils import get_or_set_order_session


# ------------------------------------------------------------------------
# Esta funcion nos devuelve todas las categorias
# ------------------------------------------------------------------------

def categorias(request):
    return render(request, "tienda/categorias.html",
                  {
                      "telefono": Informacion_empresa.objects.get(identificador="Numero de telefono"),
                      "email": Informacion_empresa.objects.get(identificador="Email"),
                      "ubicacion": Informacion_empresa.objects.get(identificador="Ubicacion"),

                      "categorias": Categorias_productos.objects.all
                  })



# ------------------------------------------------------------------------
# Esta funcion nos devuelve todos los productos de una categoria concreta
# ------------------------------------------------------------------------

def categoria_filtrada(request, slug):
    return render(request, "tienda/categoria_filtrada.html",
                  {
                      "telefono": Informacion_empresa.objects.get(identificador="Numero de telefono"),
                      "email": Informacion_empresa.objects.get(identificador="Email"),
                      "ubicacion": Informacion_empresa.objects.get(identificador="Ubicacion"),

                      "Empresas_apoyo": Empresas_apoyo.objects.all,
                      "productos": Productos.objects.filter(categoria_slug=slug)
                  })



# ------------------------------------------------------------------------
# Funcion que devuelve los detalles de un producto concreto
# ------------------------------------------------------------------------

class ProductDetailView(generic.FormView):
    template_name = "tienda/producto_detallado.html"
    form_class = AnadirAlCarrito

    def get_object(self):
        return get_object_or_404(Productos, slug=self.kwargs["slug"])

    def get_success_url(self):
        return reverse("tienda:resumen-carrito")

    def get_form_kwargs(self):
        kwargs = super(ProductDetailView, self).get_form_kwargs()
        kwargs["productos_id"] = self.get_object().id
        return kwargs

    def form_valid(self, form):
        pedido = get_or_set_order_session(self.request)
        producto = self.get_object()

        producto_filtrado = pedido.items.filter(producto=producto)

        # Si ya existia solo hay que sumar la cantidad
        if producto_filtrado.exists():
            item = producto_filtrado.first()
            item.cantidad += int(form.cleaned_data['cantidad'])
            item.save()

        # Si no existia hay que meterlo en el carrito
        else:
            # Esta añadiendo al carrito pero no hacemos commit ya que aun no ha hecho el pedido
            new_item = form.save(commit=False)
            new_item.producto = producto
            new_item.pedido = pedido
            new_item.save()

        return super(ProductDetailView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['producto'] = self.get_object()
        context['telefono'] = Informacion_empresa.objects.get(
            identificador="Numero de telefono")
        context['email'] = Informacion_empresa.objects.get(
            identificador="Email")
        context['ubicacion'] = Informacion_empresa.objects.get(
            identificador="Ubicacion")
        context['categoria'] = Productos.objects.filter(slug=(self.get_object()).slug).get(
            categoria_slug=(self.get_object()).categoria_slug)
        context['productos_categoria'] = Productos.objects.filter(categoria_slug=(
            self.get_object()).categoria_slug).exclude(slug=(self.get_object()).slug)

        return context



# ------------------------------------------------------------------------
# Funcion que devuelve el carrito de la compra
# ------------------------------------------------------------------------

class CarritoView(generic.TemplateView):
    template_name = "tienda/resumen-carrito.html"

    def get_context_data(self, *args, **kwargs):
        context = super(CarritoView, self).get_context_data(**kwargs)
        context["pedido"] = get_or_set_order_session(self.request)
        return context



# ------------------------------------------------------------------------
# Funcion que incrementa 1 unidad la cantidad de un item de la compra
# ------------------------------------------------------------------------

class IncrementarCantidadView(generic.View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(ItemPedido, id=kwargs['pk'])
        order_item.cantidad += 1
        order_item.save()
        return redirect("tienda:resumen-carrito")



# ------------------------------------------------------------------------
# Funcion que decrementa 1 unidad la cantidad de un item de la compra
# ------------------------------------------------------------------------ 

class DecrementarCantidadView(generic.View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(ItemPedido, id=kwargs['pk'])

        if order_item.cantidad <= 1:
            order_item.delete()
        else:
            order_item.cantidad -= 1
            order_item.save()
        return redirect("tienda:resumen-carrito")



# ------------------------------------------------------------------------
# Funcion que elimina completamente un item de la compra
# ------------------------------------------------------------------------

class EliminarDelCarritoView(generic.View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(ItemPedido, id=kwargs['pk'])
        order_item.delete()
        return redirect("tienda:resumen-carrito")


# ------------------------------------------------------------------------
# Funcion de checkout
# ------------------------------------------------------------------------
