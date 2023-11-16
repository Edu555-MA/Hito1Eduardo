
import re
from colorama import Fore, Style

# Función para imprimir la portada
def imprimir_portada():
    print(Fore.GREEN + Style.BRIGHT + "***********************************************************************************************************")
    print("*  ██████████   ██   ███████   ███       ██   ████      ██████████          ██████   ████      ██    ██  * ")
    print("*      ██            ██        ██  █     ██   ██  ██    ██      ██          ██       ██  ██    ██    ██  * ")
    print("*      ██       ██   ██ ██     ██    █   ██   ██    ██  ██████████          ████     ██   ██   ██    ██  * ")
    print("*      ██       ██   ██        ██      █ ██   ██  ██    ██      ██          ██       ██  ██    ██    ██  * ")
    print("*      ██       ██   ███████   ██        ██   ████      ██      ██          ██████   ████      ████████  * ")
    print("***********************************************************************************************************")
    print("Hito Eduardo Muñoz Aldanas")
    print("**************************")
    print("Proceso de Registro:" + Style.RESET_ALL)


class Cliente:
    def __init__(self, nombre, apellidos, nacionalidad, direccion, correo, telefono, tiene_tarjeta_socio=False):
        self.nombre = nombre
        self.apellidos = apellidos
        self.nacionalidad = nacionalidad
        self.direccion = direccion
        self.correo = correo
        self.telefono = telefono
        self.tiene_tarjeta_socio = tiene_tarjeta_socio
        self.lista_deseos = []


class Producto:
    def __init__(self, nombre, precio, unidades):
        self.nombre = nombre
        self.precio = precio
        self.unidades = unidades


def obtener_nacionalidad():
    while True:
        mostrar_nacionalidades()
        opcion = input("Ingrese el número correspondiente a su nacionalidad: ")
        if opcion.isdigit() and 1 <= int(opcion) <= 6:
            return int(opcion)
        else:
            print("Opción no válida. Por favor, ingrese un número del 1 al 6.")


def mostrar_nacionalidades():
    print("Lista de nacionalidades disponibles:")
    print("1. Español")
    print("2. Francés")
    print("3. Alemana")
    print("4. Andorrana")
    print("5. China")
    print("6. Otra")


def obtener_tasa_iva(nacionalidad):
    if nacionalidad == 1:
        return 21.0  # Tasa de IVA para España
    elif nacionalidad == 2:
        return 20.0  # Tasa de IVA para Francia
    elif nacionalidad == 3:
        return 17.0  # Tasa de IVA para Alemania
    elif nacionalidad == 4:
        return 7.0  # Tasa de IVA para Andorra
    elif nacionalidad == 5:
        return 14.0  # Tasa de IVA para China
    else:
        return float(input("Ingrese la tasa de IVA aplicable en su país: "))


def mostrar_productos(productos):
    print(Fore.GREEN + "Lista de productos disponibles:")
    print("{:<10} {:<20} {:<10} {:<30}".format("Índice", "Nombre", "Precio (€)", "Unidades-disponibles"))
    print("-" * 75 + Style.RESET_ALL)

    for i, (nombre, producto) in enumerate(productos.items(), start=1):
        print(Fore.GREEN + "{:<10} {:<20} {:<10} {:<30}".format(str(i), nombre, str(producto.precio),
                                                                 str(producto.unidades)) + Style.RESET_ALL)


def mostrar_inventario(productos_disponibles):
    print("\nInventario actualizado:")
    for nombre, producto in productos_disponibles.items():
        print(f"{nombre}: Unidades-disponibles: {producto.unidades}")


def obtener_metodo_pago():
    print("\nMétodos de pago disponibles:")
    print("1. Bizum")
    print("2. Tarjeta")
    print("3. PayPal")

    while True:
        opcion = input("Seleccione el método de pago (1, 2 o 3): ")
        if opcion in ['1', '2', '3']:
            return opcion
        else:
            print("Opción no válida. Por favor, seleccione 1, 2 o 3.")


def obtener_datos_tarjeta():
    numero_tarjeta = input("Ingrese el número de la tarjeta: ")
    return numero_tarjeta


def generar_factura(cliente, productos_disponibles, productos_seleccionados, nacionalidad_elegida):
    subtotal = sum([producto["producto"].precio * producto["cantidad"] for producto in productos_seleccionados])

    tasa_iva = obtener_tasa_iva(nacionalidad_elegida)

    iva = subtotal * (tasa_iva / 100)
    total_factura = subtotal + iva

    # Aplicar descuento del 2% si tiene tarjeta de socio
    if cliente.tiene_tarjeta_socio:
        descuento = total_factura * 0.02
        total_factura -= descuento
        print("Descuento de socio aplicado: 2%")

    print(Fore.GREEN + "---------Carrito de compra---------" + Style.RESET_ALL)

    # Muestra los productos seleccionados
    for producto in productos_seleccionados:
        print(f"{producto['producto'].nombre}: {producto['producto'].precio}€ - Cantidad: {producto['cantidad']}")
    print(Fore.GREEN + "---------Factura---------" + Style.RESET_ALL)
    # Muestra la factura
    print(f"Cliente: {cliente.nombre}")
    print(f"Dirección: {cliente.direccion}")
    print(f"Correo: {cliente.correo}")
    print(f"Teléfono: {cliente.telefono}")
    print(Fore.GREEN + "---------Total de compra---------" + Style.RESET_ALL)
    print(f"\nSubtotal: {subtotal:.2f}€")
    print(f"IVA ({tasa_iva}%): {iva:.2f}€")
    print(f"Total: {total_factura:.2f}€")

    # Devolver valores para usar en el mensaje adicional
    return subtotal, iva, total_factura


def enviar_mensaje(cliente, codigo_seguimiento, via_sms, direccion):
    if via_sms:
        mensaje = f"Su pedido ha sido enviado a {direccion}. Código de seguimiento: {codigo_seguimiento}"
        enviar_sms(cliente.telefono, mensaje)
    else:
        mensaje = f"Gracias por su compra. En el adjunto encontrará la factura y el código de seguimiento: {codigo_seguimiento}"
        enviar_correo(cliente.correo, "Factura del Pedido", mensaje)


def enviar_sms(numero, mensaje):
    print(f"Enviando SMS al número {numero}: {mensaje}")


def enviar_correo(correo, asunto, mensaje):
    print(f"Enviando correo a {correo} (Asunto: {asunto}): {mensaje}")


def enviar_factura_en_pdf(cliente, productos_seleccionados, subtotal, iva, total_factura):
    # Aquí podrías implementar la lógica para generar un archivo PDF de la factura y enviarlo al correo del cliente.
    # Por ahora, solo simularemos el envío del PDF imprimiendo un mensaje.
    print(f"Enviando PDF de la factura al correo {cliente.correo}")


def ingresar_correo():
    while True:
        correo = input("Ingrese su correo electrónico: ")
        if re.match(r"[^@]+@[^@]+\.[^@]+", correo):
            return correo
        else:
            print("El correo electrónico no tiene un formato válido. Inténtelo de nuevo.")


def tarea():
    datos_ingresados = False

    while True:
        if not datos_ingresados:
            nombre = input("Ingrese su nombre: ")
            apellidos = input("Ingrese sus apellidos: ")
            direccion = input("Ingrese su dirección: ")
            correo = ingresar_correo()  # Utiliza la función para validar el correo
            telefono = input("Ingrese su número de teléfono: ")

            productos_disponibles = {
                "Zapatos": Producto("Zapatos", 25.0, 10),
                "Zapatillas": Producto("Zapatillas", 55.0, 15),
                "Camisetas": Producto("Camisetas", 30.0, 20),
                "Camisas": Producto("Camisas", 18.0, 25),
                "Abrigo": Producto("Abrigo", 95.0, 12),
                "Sudadera": Producto("Sudadera", 50.0, 18),
            }

            mostrar_nacionalidades()
            nacionalidad_elegida = int(input("Ingrese el número correspondiente a su nacionalidad: "))

            # Lista para almacenar los productos seleccionados con sus cantidades
            productos_seleccionados = []
            while True:
                mostrar_productos(productos_disponibles)
                seleccion = input("Ingrese el número del producto deseado (o 'fin' para finalizar): ")

                if seleccion.lower() == 'fin':
                    break
                elif seleccion.isdigit() and 1 <= int(seleccion) <= len(productos_disponibles):
                    cantidad = int(
                        input(f"Ingrese la cantidad de '{list(productos_disponibles.keys())[int(seleccion) - 1]}': "))
                    producto_elegido = productos_disponibles[list(productos_disponibles.keys())[int(seleccion) - 1]]

                    if cantidad > producto_elegido.unidades:
                        print("No hay suficientes unidades disponibles.")
                    else:
                        productos_seleccionados.append({"producto": producto_elegido, "cantidad": cantidad})
                        producto_elegido.unidades -= cantidad
                else:
                    print("Selección no válida. Por favor, elija un número de producto de la lista.")

            tiene_tarjeta_socio = input("¿Tiene tarjeta de socio? Ingrese 'si' o 'no': ").lower() == 'si'

            # Pregunta por el método de pago
            metodo_pago = obtener_metodo_pago()

            # Solicitar información de tarjeta para todos los métodos de pago
            if metodo_pago in ['1', '2', '3']:
                numero_tarjeta = obtener_datos_tarjeta()

            # Si el método de pago es tarjeta o PayPal, solicita información adicional
            if metodo_pago in ['2', '3']:
                if metodo_pago == '2':  # Tarjeta
                    # Aquí podrías agregar lógica específica para la tarjeta si es necesario
                    pass
                elif metodo_pago == '3':  # PayPal
                    # Aquí podrías agregar lógica específica para PayPal si es necesario
                    pass

            cliente = Cliente(nombre, apellidos, nacionalidad_elegida, direccion, correo, telefono, tiene_tarjeta_socio)
            datos_ingresados = True

        subtotal, iva, total_factura = generar_factura(cliente, productos_disponibles, productos_seleccionados,
                                                        nacionalidad_elegida)

        # Mostrar productos y cantidades actualizadas después de la compra
        mostrar_inventario(productos_disponibles)

        codigo_seguimiento = "ABC123"

        eleccion = input(
            "¿Cómo desea recibir el código de seguimiento de su pedido? Ingrese 'SMS' o 'correo': ").lower()

        if eleccion == 'sms':
            via_sms = True
        elif eleccion == 'correo':
            via_sms = False
        else:
            print("Opción no válida. Se enviará por defecto por SMS.")
            via_sms = True

        enviar_mensaje(cliente, codigo_seguimiento, via_sms, cliente.direccion)

        print("Gracias por su compra.")

        # Agrega un mensaje adicional indicando que se envió el PDF al correo del cliente.
        enviar_factura_en_pdf(cliente, productos_seleccionados, subtotal, iva, total_factura)
        print("PDF de la factura enviado al correo.")

        break

# Llamar a la función de la portada
imprimir_portada()

