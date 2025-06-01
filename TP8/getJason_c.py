
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


# Clase que representa una cuenta (por token)
class CuentaConcreta:
    def __init__(self, nombre, saldo_inicial):
        self.nombre = nombre  # "token1" o "token2"
        self.saldo = saldo_inicial
        self.token_manager = TokenManager()

    def realizar_pago(self, numero_pedido, monto):
        if self.saldo >= monto:
            self.saldo -= monto
            token_usado = self.token_manager.get_token(self.nombre)
            print(f"[Pedido {numero_pedido}] Pago de ${monto} realizado con token '{self.nombre}' → clave: {token_usado}")
            return True
        else:
            print(f"[Pedido {numero_pedido}] Saldo insuficiente en '{self.nombre}' para pagar ${monto}")
            return False


# Prueba del funcionamiento

if __name__ == "__main__":
    # Crear dos cuentas con los saldos iniciales
    cuenta1 = CuentaConcreta("token1", 1000)
    cuenta2 = CuentaConcreta("token2", 2000)

    # Simulación de pagos
    cuenta1.realizar_pago(1, 500)
    cuenta2.realizar_pago(2, 500)
    cuenta1.realizar_pago(3, 600)  # Este debería fallar por saldo insuficiente
