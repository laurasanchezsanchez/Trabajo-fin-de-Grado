from django.shortcuts import render
from .models import Categorias_productos, ItemPedido
from .models import Productos, Direccion

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
from .forms import AnadirAlCarrito, DireccionForm
from .utils import get_or_set_order_session, get_pedidos_session
from django.contrib import messages


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
                      "categoria": Categorias_productos.objects.filter(slug=slug).first(),
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
        order_item.save(force_update=True, update_fields=['cantidad'])
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

class CheckoutView(generic.FormView):
    template_name = 'tienda/checkout.html'
    form_class = DireccionForm

    # Si esta todo correcto, le da a pagar y nos dirige al html de pago
    def get_success_url(self):
        return reverse("tienda:resumen-carrito")


    # D
    def form_valid(self, form):

        # Primero cogemos el pedido del cliente
        order = get_or_set_order_session(self.request)
        direccion_envio_seleccionada = form.cleaned_data.get('direccion_envio_seleccionada')
        direccion_facturacion_seleccionada = form.cleaned_data.get('direccion_facturacion_seleccionada')

        # Si el cliente ha podido seleccionar una de sus direcciones, la guardamos en el pedido
        if direccion_envio_seleccionada:
            order.direccion_envio = direccion_envio_seleccionada

        # Si no tenia ninguna guardada, se crea una direccion asociada a él
        else:
            address = Direccion.objects.create(
                direccion_tipo = 'E',
                user = self.request.user,
                direccion_1=form.cleaned_data['direccion_envio_1'],
                direccion_2=form.cleaned_data['direccion_envio_2'],
                codigo_zip=form.cleaned_data['codigo_zip_envio'],
                ciudad=form.cleaned_data['ciudad_envio'],
            )
            order.direccion_envio = address

        if direccion_facturacion_seleccionada:
            order.direccion_facturacion = direccion_facturacion_seleccionada
        else:
            address = Direccion.objects.create(
                direccion_tipo = 'F',
                user = self.request.user,
                direccion_1=form.cleaned_data['direccion_facturacion_1'],
                direccion_2=form.cleaned_data['direccion_facturacion_2'],
                codigo_zip=form.cleaned_data['codigo_zip_facturacion'],
                ciudad=form.cleaned_data['ciudad_facturacion'],
            )
            order.direccion_facturacion = address

        # Hacemos el save para cualquier opcion anterior
        order.save()
        messages.info(
            self.request, "Usted ha rellenado todos los campos correctamente.")
        return super(CheckoutView, self).form_valid(form)



    # Le pasamos al html los datos necesarios
    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        context['pedido'] = get_or_set_order_session(self.request)
        return context

    # Le pasamos al formulario el id del usuario
    def get_form_kwargs(self):
        kwargs = super(CheckoutView, self).get_form_kwargs()
        kwargs["user_id"] = self.request.user.id
        return kwargs


    
class MisPedidosView(generic.TemplateView):
    template_name = "tienda/pedidos_cliente.html"

    def get_context_data(self, *args, **kwargs):
        context = super(MisPedidosView, self).get_context_data(**kwargs)
        ped = get_pedidos_session(self.request)
        context["pedidos"] = ped
        return context