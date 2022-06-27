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
        cuerpo_mensaje = cl_data.get('mensaje')
        subject = "[FMSecom] Hemos recibido tu mensaje correctamente"

        msg = f'Hola, {nombre}. \n'
        msg = f'Su mensaje: \n"{cuerpo_mensaje}" \nha sido recibido correctamente a FMSecom. \n'
        msg += f'Le responderemos lo antes posible. \nGracias por confiar en FMSecom\n'
        msg += f'\n\n\nEste mensaje y sus anexos pueden contener información confidencial, por lo que se informa de que su uso no autorizado está prohibido por la ley. Si Vd. considera que no es el destinatario pretendido por el remitente o no desea recibir información comercial, por favor póngalo en su conocimiento por esta misma vía o por cualquier otro medio y elimine esta comunicación y los anexos de su sistema, sin copiar, remitir o revelar los contenidos del mismo a cualquier otra persona. Cualquier información, opinión, conclusión, recomendación, etc. contenida en el presente mensaje no relacionada con la actividad empresarial de DOMINGO SANCHEZ MARIN y/o emitida por persona sin capacidad para ello, deberá considerarse como no proporcionada ni aprobada por DOMINGO SANCHEZ MARIN pone los medios a su alcance para garantizar la seguridad y ausencia de errores en la correspondencia electrónica, pero no puede asegurar la inexistencia de virus o la no alteración de los documentos transmitidos electrónicamente, por lo que declina cualquier responsabilidad a este respecto.'
        return subject, msg, email_cliente

    def send(self):

        subject, msg = self.get_info()

        send_mail(
            subject=subject,
            message=msg,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER]
        )

    def send_confirmation(self):

        subject, msg, email_cliente = self.get_info_confirmation()

        send_mail(
            subject=subject,
            message=msg,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email_cliente, ]
        )
