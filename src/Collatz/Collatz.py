import matplotlib.pyplot as plt

def collatz_steps(n):
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps

# Calcular la cantidad de iteraciones para cada número del 1 al 10,000
x_values = list(range(1, 10001))
y_values = [collatz_steps(n) for n in x_values]

# Graficar
plt.figure(figsize=(10, 6))
plt.scatter(y_values, x_values, s=1, color='blue')
plt.xlabel("Número de iteraciones")
plt.ylabel("Número inicial de la secuencia")
plt.title("Número de iteraciones para converger en la secuencia de Collatz")
plt.grid()
plt.show()
