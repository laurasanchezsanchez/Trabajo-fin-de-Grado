from django import template
from tienda.utils import get_or_set_order_session

# Para que haga la cuenta de productos que tiene el cliente y salga como numero pequeño arriba

register = template.Library()

@register.filter
def count_items(request):
    pedido = get_or_set_order_session(request)
    count = pedido.items.count()
    return count