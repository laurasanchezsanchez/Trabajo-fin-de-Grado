from datetime import datetime
from django.core.mail import send_mail
from django.shortcuts import render
from .models import Categorias_productos, ItemPedido, Pedido
from .models import Productos, Direccion
from django.conf import settings

# añadido para cambiar de vistas
from dataclasses import fields
from pdb import post_mortem
from django.shortcuts import get_object_or_404, reverse, redirect
from django.views import generic
from .forms import AnadirAlCarrito, DireccionForm
from .utils import get_or_set_order_session, get_pedidos_session, enviar_confirmacion_pedido, enviar_pedido_realizado_fmsecom
from django.contrib import messages


from django.conf import settings  # new
from django.http.response import JsonResponse  # new
from django.views.decorators.csrf import csrf_exempt  # new
from django.views.generic.base import TemplateView

import stripe
stripe.api_key = "sk_test_51L8KiTGoxA9pTzWIYBbDEpGchhaj9hA4r3nDiMEYCOVodnJdzto6VYbwTNuTnBke1mrQyHepzuOptnP62b5pAeUL00epOSUraP"
# ------------------------------------------------------------------------
# Esta funcion nos devuelve todas las categorias
# ------------------------------------------------------------------------


def categorias(request):
    return render(request, "tienda/categorias.html",
                  {
                      "categorias": Categorias_productos.objects.all,
                      "productos": Productos.objects.all
                  })


# ------------------------------------------------------------------------
# Esta funcion nos devuelve todos los productos de una categoria concreta
# ------------------------------------------------------------------------

def categoria_filtrada(request, slug):
    return render(request, "tienda/categoria_filtrada.html",
                  {
                      "categoria": Categorias_productos.objects.filter(slug=slug).first(),
                      "productos": Productos.objects.filter(categoria_slug=slug)
                  })


# ------------------------------------------------------------------------
# Funcion que devuelve los detalles de un producto concreto.
# Al darle a añadir le lleva a la pagina del carrito
# ------------------------------------------------------------------------

class ProductDetailView(generic.FormView):
    template_name = "tienda/producto_detallado.html"
    form_class = AnadirAlCarrito

    def get_object(self):
        return get_object_or_404(Productos, slug=self.kwargs["slug"])

    # Al darle a añadir le lleva a la pagina del carrito
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
    # Como aun no tengo html de pago, lo redirijo al resumen del carrito otra vez
    def get_success_url(self):
        return reverse("tienda:payment")

    def get_cancel_url(self):
        return reverse("tienda:categoria")

    def form_valid(self, form):

        # Primero cogemos el pedido del cliente
        order = get_or_set_order_session(self.request)
        direccion_envio_seleccionada = form.cleaned_data.get(
            'direccion_envio_seleccionada')
        direccion_facturacion_seleccionada = form.cleaned_data.get(
            'direccion_facturacion_seleccionada')
        order.realizado = False

        # Si el cliente ha podido seleccionar una de sus direcciones, la guardamos en el pedido
        if direccion_envio_seleccionada:
            order.direccion_envio = direccion_envio_seleccionada

        # Si no tenia ninguna guardada, se crea una direccion asociada a él
        else:
            address = Direccion.objects.create(
                direccion_tipo='E',
                user=self.request.user,
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
                direccion_tipo='F',
                user=self.request.user,
                direccion_1=form.cleaned_data['direccion_facturacion_1'],
                direccion_2=form.cleaned_data['direccion_facturacion_2'],
                codigo_zip=form.cleaned_data['codigo_zip_facturacion'],
                ciudad=form.cleaned_data['ciudad_facturacion'],
            )
            order.direccion_facturacion = address

        # Hacemos el save para cualquier opcion anterior
        order.save()

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



class PaymentView(generic.TemplateView):
    template_name = 'tienda/payment.html'

    def get_context_data(self, *args, **kwargs):
        context = super(PaymentView, self).get_context_data(**kwargs)
        context["pedido"] = get_or_set_order_session(self.request)
        return context


# #########################################################################
# #########################################################################
# ############################ stripe #####################################
# #########################################################################
# #########################################################################

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        pedido = get_or_set_order_session(request)
        cantidad = pedido.get_total()
        enviar_confirmacion_pedido(request)
        enviar_pedido_realizado_fmsecom(request)
        pedido.realizado = True
        pedido.fecha = datetime.now()
        pedido.save()
        

        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url +
                'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': 'CamaraPrueba',
                        'quantity': 1,
                        'currency': 'eur',
                        'amount': round(cantidad)*100,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})



class SuccessView(generic.View):
    def post(self, request, *args, **kwargs):
        pedido = get_or_set_order_session(request)
        pedido.realizado = True
        pedido.fecha = datetime.date.today()
        pedido.save()
        #enviar_confirmacion_pedido()
        return redirect("tienda/success.html")

class CancelledView(TemplateView):
    template_name = 'tienda/cancelled.html'


# Search
def search(request):
	q=request.GET['q']
	data=Productos.objects.filter(nombre__icontains=q).order_by('-id')
	return render(request,'tienda/search.html',{'data':data})



def detallesPedido(request, pk):
    return render(request, "tienda/detalles_pedido.html",
                  {
                      "pedido": Pedido.objects.filter(pk=pk).first(),
                  })