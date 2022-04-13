from .models import Pedido


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
