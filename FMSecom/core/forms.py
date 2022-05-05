from django import forms

# Define el formulario de Contacto
class ContactForm(forms.Form):
    nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': "Tu Nombre"
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': "Tu Correo Electronico"
    }))
    mensaje = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Tu Mensaje"
    }))