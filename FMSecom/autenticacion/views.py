from django.shortcuts import redirect
from django.shortcuts import render, reverse
from django.views.generic import View

# Nos construye el formulario, la otra el de login
from django.contrib.auth.forms import AuthenticationForm

# Poder hacer login y logout. El authenticate es el que nos permite ver si ha hecho bien la autenticacion
from django.contrib.auth import login, logout, authenticate

# Para mostrar los mensajes de error al hacer mal el registro
from django.contrib import messages

from django.contrib.auth.views import PasswordChangeView
from .forms import CambiarPasswordForm, UserCreationForm


# Create your views here.
class VistaRegistro(View):

    # Nos renderiza/muestra el formulario
    def get(self, request):
        form = UserCreationForm
        return render(request, "registro/registro.html", {"form": form})

    # Envia los datos a la bd

    def post(self, request):
        form = UserCreationForm(request.POST)

        # Como el formulario si metemos solo numeros por ejemplo puede fallar, metemos condicion

        if form.is_valid():
            # Con form.save guardo la informacion en la bd
            user = form.save()

            # Una vez registrado lo dejamos logeado
            login(request, user)

            return redirect('/')

        else:
            # Para cada mensaje de error que haya en el form - muestralo
            for msg in form.error_messages:
                # Los mensajes iran en la peticion y le mandamos justo ese mensaje (error_messages es un array)
                messages.error(request, form.error_messages[msg])

            return render(request, "registro/registro.html", {"form": form})


def cerrar_sesion(request):
    logout(request)

    return redirect('/')


def loguear(request):

    # Si le has dado al boton
    if request.method == "POST":
        # En form guardar los datos del formulario
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            nombre_user = form.cleaned_data.get("username")
            contra = form.cleaned_data.get("password")

            # Si authenticate ve que no es correcto el user, no nos devuelve nada, por lo que haremos el proximo if
            user = authenticate(username=nombre_user, password=contra)

            if user is not None:
                login(request,user)
                return redirect('/')
            else:
                messages.error(request, "user no valido")

        else:
            messages.error(request, "Informacion incorrecta.")

    form = AuthenticationForm()
    return render(request, "login/login.html", {"form": form})


class perfilView(PasswordChangeView):
    form_class = CambiarPasswordForm
    template_name = 'usuario/perfil.html'

    def get_success_url(self):
        return reverse('autenticacion:password_success')


def password_success(request):
    return render(request, "usuario/password_success.html", {})
