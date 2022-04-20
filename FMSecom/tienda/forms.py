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



class DireccionForm(forms.Form):

    # Campos a rellenar
    direccion_envio_1 = forms.CharField(required=False)
    direccion_envio_2 = forms.CharField(required=False)
    codigo_zip_envio = forms.CharField(required=False)
    ciudad_envio = forms.CharField(required=False)

    direccion_facturacion_1 = forms.CharField(required=False)
    direccion_facturacion_2 = forms.CharField(required=False)
    codigo_zip_facturacion = forms.CharField(required=False)
    ciudad_facturacion = forms.CharField(required=False)

    # Crearemos un choice por si tienen ya registradas sus direcciones
    direccion_envio_seleccionada = forms.ModelChoiceField(
        Direccion.objects.none(), required=False
    )

    direccion_facturacion_seleccionada = forms.ModelChoiceField(
        Direccion.objects.none(), required=False
    )

    # Ahora filtraremos los datos a ese cliente
    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id')
        super().__init__(*args, **kwargs)

        # Filtramos los datos para ese usuario
        user = User.objects.get(id=user_id)

        # Sentencias para obtener sus direcciones guardadas
        direccion_envio_qs = Direccion.objects.filter(
            user=user,
            direccion_tipo='E'
        )

        direccion_facturacion_qs = Direccion.objects.filter(
            user=user,
            direccion_tipo='F'
        )

        # Para que aparezcan como opciones
        self.fields['direccion_envio_seleccionada'].queryset = direccion_envio_qs
        self.fields['direccion_facturacion_seleccionada'].queryset = direccion_facturacion_qs

    
    # Limpiamos los datos del formulario - si no se rellena algun campo, definimos el error
    def clean(self):

        # Si los datos no son validos, cleaned data solo se queda con los validos
        data = self.cleaned_data

        direccion_envio_seleccionada = data.get('direccion_envio_seleccionada', None)
        if direccion_envio_seleccionada is None:
            if not data.get('direccion_envio_1', None):
                self.add_error("direccion_envio_1", "Por favor, rellene este campo")
            if not data.get('direccion_envio_2', None):
                self.add_error("direccion_envio_2", "Por favor, rellene este campo")
            if not data.get('codigo_zip_envio', None):
                self.add_error("codigo_zip_envio", "Por favor, rellene este campo")
            if not data.get('ciudad_envio', None):
                self.add_error("ciudad_envio", "Por favor, rellene este campo")

        direccion_facturacion_seleccionada = data.get('direccion_facturacion_seleccionada', None)
        if direccion_facturacion_seleccionada is None:
            if not data.get('direccion_facturacion_1', None):
                self.add_error("direccion_facturacion_1", "Por favor, rellene este campo")
            if not data.get('direccion_facturacion_2', None):
                self.add_error("direccion_facturacion_2", "Por favor, rellene este campo")
            if not data.get('codigo_zip_facturacion', None):
                self.add_error("codigo_zip_facturacion", "Por favor, rellene este campo")
            if not data.get('ciudad_facturacion', None):
                self.add_error("ciudad_facturacion", "Por favor, rellene este campo")

