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
    
    msg += f'\n\n Gracias por confiar en FMSecom\n'
    msg += f'\n\n\nEste mensaje y sus anexos pueden contener información confidencial, por lo que se informa de que su uso no autorizado está prohibido por la ley. Si Vd. considera que no es el destinatario pretendido por el remitente o no desea recibir información comercial, por favor póngalo en su conocimiento por esta misma vía o por cualquier otro medio y elimine esta comunicación y los anexos de su sistema, sin copiar, remitir o revelar los contenidos del mismo a cualquier otra persona. Cualquier información, opinión, conclusión, recomendación, etc. contenida en el presente mensaje no relacionada con la actividad empresarial de DOMINGO SANCHEZ MARIN y/o emitida por persona sin capacidad para ello, deberá considerarse como no proporcionada ni aprobada por DOMINGO SANCHEZ MARIN pone los medios a su alcance para garantizar la seguridad y ausencia de errores en la correspondencia electrónica, pero no puede asegurar la inexistencia de virus o la no alteración de los documentos transmitidos electrónicamente, por lo que declina cualquier responsabilidad a este respecto.'


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


