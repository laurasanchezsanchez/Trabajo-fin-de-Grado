# Trabajo de Fin de Grado - Laura Sánchez Sánchez

### Universidad de Granada. Ingeniería Informática
##### _Desarrollo de una herramienta software para la gestión y ejecución de ventas sin depender del espacio físico_
---

###### Palabras clave:
Servicios Cloud, Programación Aplicaciones Web, Docker, Django, Python

### Proyecto

###### Resumen del proyecto
En este proyecto se diseña e implementa una **herramienta capaz de generar ventas de productos y servicios de una empresa** concreta, independientemente del lugar donde se realice, se consigue un control exhaustivo de la administración de la misma y gestiona a los clientes para ofrecer un trato más personalizado de forma automática.

###### Tecnologías utilizadas
- Scrum como metodología ágil
- Django (4.0.2) y paquetes adicionales del mismo
- Sqlite3 como base de datos
- Anaconda Navigator
- HyperText Markup Language (HTML), Cascading Style Sheets (CSS) y JavaScript (JS)
- Stripe como pasarela de pago

###### Funcionalidad
El usuario se puede dar de alta en la plataforma rellenando un formulario y creando su propia contraseña que se almacenará de manera encriptada para garantizar su seguridad. Una vez registrado el usuario puede realizar compras en la plataforma.
Al realizar la compra se envía automáticamente un mensaje por correo electrónico al cliente y al empresario con la confirmación del pedido.
Los clientes tendrán un apartado donde podrán ver todos los pedidos que han realizado.
Además, cualquier usuario no registrado puede enviar un mensaje al empresario a través de esta plataforma.
Por último, el administrador encargado de la plataforma podrá personalizar cualquier parte de ésta a partir de un panel de administración. En este panel también puede agregar, modificar o eliminar cualquier producto a la venta y dar soporte a cualquier problema relacionado con los pedidos de los clientes.


### ¿Cómo puedo probar este proyecto?
1. Descargue este proyecto
2. Instale Anaconda Navigator
3. En Anaconda Navigator cree un nuevo Environment de Python (última versión)
4. Inicie el Environment
5. Diríjase dentro del entorno a la carpeta donde haya descargado este proyecto
6. Cree un archivo llamado .env y rellene los siguientes campos:
    - SECRET_KEY = 'SECRET_KEY'
    - DEBUG = True
    - EMAIL_HOST = 'EMAIL_HOST'
    - EMAIL_PORT = EMAIL_PORT
    - EMAIL_HOST_USER = 'EMAIL_HOST_USER'
    - EMAIL_HOST_PASSWORD = 'EMAIL_HOST_PASSWORD'
    - STRIPE_PUBLISHABLE_KEY = 'STRIPE_PUBLISHABLE_KEY'
    - STRIPE_SECRET_KEY = 'STRIPE_SECRET_KEY'
7. Introduzca en la shell:
    ```sh
    pip install -r requirements.txt
    py manage.py makemigrations
    py manage.py migrate
    python manage.py runserver
    ```
8. Ingrese en su navegador __localhost:8000__
