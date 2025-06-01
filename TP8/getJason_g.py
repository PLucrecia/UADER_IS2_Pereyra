"""
TP8 - Ingeniería de Software II - Punto (g)
Programa para gestionar pagos automatizados con tokens bancarios.
Incluye patrón Singleton para manejo de tokens desde JSON,
patrón Cadena de Responsabilidad para asignar pagos según saldo,
y patrón Iterator para listar pagos realizados.
Versión 1.2
"""

import json
import os
import sys

VERSION = "1.2"

class TokenManager:
    """
    Singleton que carga y administra las claves de tokens bancarios
    desde un archivo JSON (sitedata.json).
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TokenManager, cls).__new__(cls)
            cls._instance._load_data()
        return cls._instance

    def _load_data(self):
        """Carga los datos del archivo JSON en un diccionario."""
        filename = 'sitedata.json'
        if not os.path.exists(filename):
            raise FileNotFoundError(f"No se encuentra el archivo {filename}.")
        with open(filename, 'r') as file:
            self.data = json.load(file)

    def get_token(self, key):
        """
        Retorna la clave asociada a un token dado.
        Lanza KeyError si el token no existe.
        """
        if key not in self.data:
            raise KeyError(f"La clave '{key}' no existe.")
        return self.data[key]

class CuentaHandler:
    """
    Clase que representa una cuenta bancaria/token con saldo.
    Implementa el patrón Cadena de Responsabilidad para procesar pagos.
    """

    def __init__(self, nombre, saldo_inicial, gestor_pagos):
        """
        Inicializa la cuenta con nombre (token), saldo y referencia al gestor de pagos.
        """
        self.nombre = nombre
        self.saldo = saldo_inicial
        self.token_manager = TokenManager()
        self.siguiente = None
        self.gestor_pagos = gestor_pagos

    def set_siguiente(self, siguiente_handler):
        """
        Define el siguiente handler en la cadena de responsabilidad.
        """
        self.siguiente = siguiente_handler

    def procesar_pago(self, numero_pedido, monto):
        """
        Intenta procesar un pago si hay saldo suficiente.
        Si no, pasa la solicitud al siguiente handler en la cadena.
        Registra el pago realizado en el gestor de pagos.
        """
        if self.saldo >= monto:
            self.saldo -= monto
            clave = self.token_manager.get_token(self.nombre)
            print(f"[Pedido {numero_pedido}] Pago de ${monto} realizado con token '{self.nombre}' → clave: {clave}")
            self.gestor_pagos.agregar_pago(numero_pedido, self.nombre, monto)
        elif self.siguiente:
            self.siguiente.procesar_pago(numero_pedido, monto)
        else:
            print(f"[Pedido {numero_pedido}] No hay cuentas con saldo suficiente para pagar ${monto}.")

class GestorPagos:
    """
    Clase que almacena todos los pagos realizados y provee un iterador
    para listarlos en orden cronológico.
    """

    def __init__(self):
        """Inicializa la lista interna de pagos."""
        self.pagos = []

    def agregar_pago(self, numero_pedido, token, monto):
        """
        Agrega un pago a la lista.
        """
        self.pagos.append({'numero_pedido': numero_pedido, 'token': token, 'monto': monto})

    def __iter__(self):
        """
        Retorna un iterador para recorrer los pagos en orden.
        """
        return iter(self.pagos)

if __name__ == "__main__":
    # Manejo de argumento para mostrar versión
    if len(sys.argv) > 1 and sys.argv[1] == "-v":
        print(f"Versión {VERSION}")
        sys.exit(0)

    # Instancia del gestor de pagos
    gestor_pagos = GestorPagos()

    # Creación de las cuentas con saldo inicial
    cuenta1 = CuentaHandler("token1", 1000, gestor_pagos)
    cuenta2 = CuentaHandler("token2", 2000, gestor_pagos)

    # Configura la cadena de responsabilidad: cuenta1 -> cuenta2
    cuenta1.set_siguiente(cuenta2)

    # Lista de montos de pagos a realizar
    pagos_a_realizar = [500, 500, 500, 500, 500]

    # Procesamiento de pagos secuenciales
    for i, monto in enumerate(pagos_a_realizar, start=1):
        cuenta1.procesar_pago(i, monto)

    # Mostrar listado cronológico de pagos realizados
    print("\nListado cronológico de pagos realizados:")
    for pago in gestor_pagos:
        print(f"Pedido {pago['numero_pedido']}: token={pago['token']}, monto=${pago['monto']}")
