
class Cuenta:
    def __init__(self, nombre, saldo):
        self.nombre = nombre
        self.saldo = saldo

    def puede_pagar(self, monto):
        return self.saldo >= monto

    def pagar(self, monto):
        self.saldo -= monto
        print(f"✅ Pago de ${monto} realizado desde {self.nombre} (saldo restante: {self.saldo})")


class SistemaBalanceado:
    def __init__(self):
        self.c1 = Cuenta("token1", 1000)
        self.c2 = Cuenta("token2", 2000)
        self.turno = True  # True = token1, False = token2

    def procesar_pago(self, monto):
        cuenta = self.c1 if self.turno else self.c2
        if cuenta.puede_pagar(monto):
            cuenta.pagar(monto)
        else:
            # Si la cuenta elegida no puede pagar, se intenta con la otra
            otra = self.c2 if self.turno else self.c1
            if otra.puede_pagar(monto):
                otra.pagar(monto)
            else:
                print("❌ No hay fondos suficientes en ninguna cuenta.")
        self.turno = not self.turno  # alterna el turno

# Prueba
if __name__ == "__main__":
    sistema = SistemaBalanceado()
    for _ in range(5):
        sistema.procesar_pago(500)
