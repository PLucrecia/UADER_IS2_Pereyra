import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

# Datos históricos
data = {
    'LOC': [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 1000],
    'Esfuerzo': [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
}
df = pd.DataFrame(data)

#----------------------------
# Modelo lineal
#----------------------------
a, b = np.polyfit(df['LOC'], df['Esfuerzo'], 1)
R = np.corrcoef(df['LOC'], df['Esfuerzo'])
R2_linear = R[0,1]**2
print("Modelo lineal: E = %.4f * LOC + %.4f, R² = %.4f" % (a, b, R2_linear))

#----------------------------
# Modelo exponencial
#----------------------------
df['logEsfuerzo'] = np.log(df['Esfuerzo'])
df['logLOC'] = np.log(df['LOC'])
X = sm.add_constant(df['logLOC'])
model_exp = sm.OLS(df['logEsfuerzo'], X).fit()
k = np.exp(model_exp.params['const'])
b_exp = model_exp.params['logLOC']
R2_exp = model_exp.rsquared
print("Modelo exponencial: E = %.4f * LOC^%.4f, R² = %.4f" % (k, b_exp, R2_exp))

#----------------------------
# Elegir mejor modelo
#----------------------------
if R2_linear >= R2_exp:
    modelo = 'lineal'
    print("Se elige el modelo LINEAL")
else:
    modelo = 'exponencial'
    print("Se elige el modelo EXPONENCIAL")

#----------------------------
# Predicciones para LOC=9100 y LOC=200
#----------------------------
LOC_values = [9100, 200]
E_values = []

for LOC_proj in LOC_values:
    if modelo == 'lineal':
        E_proj = a*LOC_proj + b
    else:
        E_proj = k * (LOC_proj ** b_exp)
    E_values.append(E_proj)
    print(f"Esfuerzo estimado para LOC={LOC_proj}: {E_proj:.2f} PM")

#----------------------------
# Graficar resultados
#----------------------------
plt.figure(figsize=(8,5))
plt.scatter(df['LOC'], df['Esfuerzo'], label='Datos históricos', color='black')

# Modelo ajustado
LOC_range = np.linspace(min(df['LOC']), max(LOC_values), 100)
if modelo == 'lineal':
    plt.plot(LOC_range, a*LOC_range+b, color='red', label=f'Modelo lineal (R²={R2_linear:.2f})')
else:
    plt.plot(LOC_range, k*LOC_range**b_exp, color='green', label=f'Modelo exponencial (R²={R2_exp:.2f})')

# Puntos de predicción
plt.scatter(LOC_values, E_values, color='blue', s=100, marker='X', label='Proyectos estimados')

plt.xlabel('Complejidad [LOC]')
plt.ylabel('Esfuerzo [PM]')
plt.title('Modelo de esfuerzo vs LOC')
plt.legend()
plt.grid(True)
plt.show()

#----------------------------
# Precaución para LOC=200
#----------------------------
print("\nPrecaución: LOC=200 está fuera del rango de calibración (datos históricos 1000-9000).")
print("La predicción puede no ser confiable y se considera una extrapolación.")
