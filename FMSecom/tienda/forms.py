from django import forms
from .models import ItemPedido, Productos, Direccion
from django.contrib.auth import get_user_model

User = get_user_model()

# --------------------------------------------------------
# Esta clase solo sumara las cantidades que el cliente desea del producto
# --------------------------------------------------------
class AnadirAlCarrito(forms.ModelForm):
    cantidad = forms.IntegerField(min_value=1)

    class Meta:
        model = ItemPedido
        fields = ['cantidad']

    def __init__(self, *args, **kwargs):
        self.productos_id = kwargs.pop('productos_id')
        productos = Productos.objects.get(id=self.productos_id)
        super().__init__(*args, **kwargs)


    def clean(self):
        productos_id = self.productos_id
        productos = Productos.objects.get(id=self.productos_id)
        cantidad = self.cleaned_data['cantidad']

        # En un pedido se pueden hacer un maximo de 200 productos iguales
        if cantidad > 200:
            raise forms.ValidationError("Lo sentimos. El maximo de productos iguales por pedido es 200.")


