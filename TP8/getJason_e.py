

import json
import os

# Singleton para acceso al JSON de tokens

class TokenManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TokenManager, cls).__new__(cls)
            cls._instance._load_data()
        return cls._instance

    def _load_data(self):
        filename = 'sitedata.json'
        if not os.path.exists(filename):
            raise FileNotFoundError(f"No se encuentra el archivo {filename}.")
        with open(filename, 'r') as file:
            self.data = json.load(file)

    def get_token(self, key):
        if key not in self.data:
            raise KeyError(f"La clave '{key}' no existe.")
        return self.data[key]

# Clase base de la cadena

class CuentaHandler:
    def __init__(self, nombre, saldo_inicial, gestor_pagos):
        self.nombre = nombre
        self.saldo = saldo_inicial
        self.token_manager = TokenManager()
        self.siguiente = None
        self.gestor_pagos = gestor_pagos  # referencia para guardar pagos

    def set_siguiente(self, siguiente_handler):
        self.siguiente = siguiente_handler

    def procesar_pago(self, numero_pedido, monto):
        if self.saldo >= monto:
            self.saldo -= monto
            clave = self.token_manager.get_token(self.nombre)
            print(f"[Pedido {numero_pedido}] Pago de ${monto} realizado con token '{self.nombre}' → clave: {clave}")
            self.gestor_pagos.agregar_pago(numero_pedido, self.nombre, monto)
        elif self.siguiente:
            self.siguiente.procesar_pago(numero_pedido, monto)
        else:
            print(f"[Pedido {numero_pedido}] No hay cuentas con saldo suficiente para pagar ${monto}.")


# Clase que gestiona pagos y provee un iterador

class GestorPagos:
    def __init__(self):
        self.pagos = []

    def agregar_pago(self, numero_pedido, token, monto):
        self.pagos.append({'numero_pedido': numero_pedido, 'token': token, 'monto': monto})

    def __iter__(self):
        # Devuelve un iterador para recorrer los pagos en orden
        return iter(self.pagos)


# Prueba del sistema

if __name__ == "__main__":
    gestor_pagos = GestorPagos()

    cuenta1 = CuentaHandler("token1", 1000, gestor_pagos)
    cuenta2 = CuentaHandler("token2", 2000, gestor_pagos)

    cuenta1.set_siguiente(cuenta2)

    pagos_a_realizar = [500, 500, 500, 500, 500]

    for i, monto in enumerate(pagos_a_realizar, start=1):
        cuenta1.procesar_pago(i, monto)

    print("\nListado cronológico de pagos realizados:")
    for pago in gestor_pagos:
        print(f"Pedido {pago['numero_pedido']}: token={pago['token']}, monto=${pago['monto']}")
