from .models import Pedido
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime

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

def enviar_confirmacion_pedido(request):
    nombre = request.user.username
    email_cliente = request.user.email
    subject = "[FMSecom] Su pedido se ha realizado correctamente"

    msg = f'Hola, {nombre}. \n'
    msg += f'Su pedido se ha realizado correctamente.\n'
    msg += f'\nDetalles de su pedido: \n'
    pedido = get_or_set_order_session(request)
    for item in pedido.items.all():
        msg += f'{item.reference_number}' 
        msg += f'\n'
    
    msg += f'\n\n Gracias por confiar en FMSecom'

    send_mail(
            subject=subject,
            message=msg,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email_cliente,]
        )
    return True


def enviar_pedido_realizado_fmsecom(request):
    pedido = get_or_set_order_session(request)
    nombre = 'FMSecom'
    email_cliente = pedido.user.email
    subject = '[FMSecom] NUEVO PEDIDO'
    fecha = datetime.now()

    msg = f'Pedido realizado por {pedido.user.username}, con el email: {email_cliente}.'
    msg += f'\n Detalles del pedido: \n'
    
    for item in pedido.items.all():
        msg += f'{item.reference_number}' 
        msg += f'\n'
    
    msg += f'\n\n Pedido realizado en fecha: {fecha}'

    send_mail(
            subject=subject,
            message=msg,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER,]
        )
    return True


