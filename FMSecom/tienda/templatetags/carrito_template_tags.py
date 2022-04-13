from django import template
from tienda.utils import get_or_set_order_session


register = template.Library()

@register.filter
def count_items(request):
    pedido = get_or_set_order_session(request)
    count = pedido.items.count()
    return count