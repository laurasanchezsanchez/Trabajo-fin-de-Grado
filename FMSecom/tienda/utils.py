from .models import Pedido
from django.core.mail import send_mail
from django.conf import settings

def get_or_set_order_session(request):
    pedido_id = request.session.get('pedido_id', None)
    if pedido_id is None:
        pedido = Pedido()
        pedido.save()
        request.session['pedido_id'] = pedido.id

    else: 
        try:
            pedido = Pedido.objects.get(id=pedido_id, realizado=False)
        except Pedido.DoesNotExist:
            pedido = Pedido()
            pedido.save()
            request.session['pedido_id'] = pedido.id

    if request.user.is_authenticated and pedido.user is None:
        pedido.user= request.user
        pedido.save()
    return pedido


def get_pedidos_session(request):
    cliente = request.user
    pedidos = Pedido.objects.filter(user=cliente, realizado=True)

    return pedidos

def enviar_confirmacion_pedido():
    nombre = 'LAURA'
    email_cliente = 'laurasanchezsanchez.lss.13@gmail.com'
    subject = "[FMSecom] Su pedido se ha realizado correctamente"

    msg = f'Hola, {nombre}. \n'
    msg += f'Su pedido se ha realizado correctamente Le responderemos lo antes posible. \n Gracias por confiar en FMSecom'

    send_mail(
            subject=subject,
            message=msg,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email_cliente,]
        )
    return True

