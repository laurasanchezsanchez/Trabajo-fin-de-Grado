from django import forms
from django.conf import settings
from django.core.mail import send_mail

# Define el formulario de Contacto
class ContactForm(forms.Form):
    nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': "Tu Nombre"
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': "Tu Correo Electronico"
    }))
    mensaje = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': "Tu Mensaje"
    }))


    def get_info(self):
        """
        Method that returns formatted information
        :return: subject, msg
        """
        # Cleaned data
        cl_data = super().clean()

        nombre = cl_data.get('nombre').strip()
        from_email = cl_data.get('email')
        subject = "Mensaje de contacto a través de FMSecom"

        msg = f'{nombre} con el email {from_email} dice: \n'
        msg += cl_data.get('mensaje')

        return subject, msg

    def get_info_confirmation(self):
        # Cleaned data
        cl_data = super().clean()

        nombre = cl_data.get('nombre').strip()
        email_cliente = cl_data.get('email')
        subject = "[FMSecom] Hemos recibido tu mensaje correctamente"

        msg = f'Hola, {nombre}. \n'
        msg += f'Su mensaje ha sido recibido correctamente. Le responderemos lo antes posible. \n Gracias por confiar en FMSecom'

        return subject, msg, email_cliente

    def send(self):

        subject, msg = self.get_info()

        send_mail(
            subject=subject,
            message=msg,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.RECIPIENT_ADDRESS]
        )

    def send_confirmation(self):

        subject, msg, email_cliente = self.get_info_confirmation()

        send_mail(
            subject=subject,
            message=msg,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email_cliente,]
        )