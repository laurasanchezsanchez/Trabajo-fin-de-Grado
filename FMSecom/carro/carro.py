class Carro:
    # Almacenamos la peticion actual para poder utilizarla en la clase
    # Almacenamos la sesion
    # Construiremos un carro para esta sesion
    # El carro será un diccionario clave-valor --> clave=id del producto, valor=todas las caracteristicas del producto
    def __init__(self, request):
        self.request=request
        self.session=request.session
        carro=self.session.get('carro')

        # Si no hay carro lo creamos vacio
        if not carro:
            carro=self.session['carro']={}
            self.carro=self.session['carro']
        # El usuario habia abandonado la pagina y vuelve
        else:
            self.carro=carro

    def guardar_carro(self):
        self.session["carro"]=self.carro
        self.session.modified=True

    # Se agregan productos que no estaban anteriormente
    def agregar(self, producto):
        if (str(producto.id) not in self.carro.keys()):
            self.carro[producto.id]={
                "producto_id":producto.id,
                "nombre":producto.nombre,
                "precio": str(producto.precio_producto),
                "cantidad":1,
                "imagen":producto.imagen1.url,
                "precio_cantidad":str(producto.precio_producto)
            }
        else:
            # Si ya estaba ese producto, aumentamos la cantidad
            for key, value in self.carro.items():
                if key == str(producto.id):
                    value["cantidad"]=value["cantidad"]+1
                    value["precio_cantidad"]=float(value["precio_cantidad"])+producto.precio_producto
                    break
        self.guardar_carro()

    

    # Primero comprobamos si ese producto esta en el carro
    # Eliminaremos un producto completo del carro (todas las unidades)
    def eliminar(self, producto):
        producto.id = str(producto.id)
        if producto.id in self.carro:
            del self.carro[producto.id]
            self.guardar_carro()

    def restar_producto(self, producto):
        for key, value in self.carro.items():
                if key == str(producto.id):
                    value["cantidad"]=value["cantidad"]-1
                    value["precio_cantidad"]=float(value["precio_cantidad"])-producto.precio_producto
                    if value["cantidad"]<1:
                        self.eliminar(producto)
                    break
        self.guardar_carro()

    def limpiar_carro(self):
        self.session["carro"]={}
        self.session.modified=True

