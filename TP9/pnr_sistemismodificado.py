#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
#* PNR_sistemis_modificado
#* Programa para procesar modelos dinámicos basado en el modelo de Putman-Norden_Rayleigh
#* Modificado para análisis comparativo con diferentes valores de esfuerzo y parámetro 'a'
#*
#* UADER - FCyT
#* Ingeniería de Software II
#*
#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
import pandas as pd
import numpy as np
import sys
import os
import math
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar
from scipy.optimize import root_scalar
from scipy.integrate import quad
import argparse

#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
#*                             Librerías y funciones de soporte
#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=

def E_proyecto(K, a, gamma):  
    """Estima el esfuerzo consumido al momento de la liberación del proyecto"""
    tf = np.sqrt(-np.log(1-gamma)/a)
    Ef = gamma*K
    return tf, Ef

def E_acum(K, a, t):
    """Calcula el esfuerzo acumulado en función del tiempo E(t)"""
    return K*(1-np.exp(-a*(t**2)))

def E(t, K, a):
    """Calcula el esfuerzo instantáneo o staff p(t) en un momento t"""
    return 2 * K * a * t * np.exp(-a * t**2)

def find_maximum(K, a):
    """Encuentra el valor máximo de la función p(t)"""
    def negative_E(t):
        return -E(t, K, a)
    
    result = minimize_scalar(negative_E, bounds=(0, 100), method='bounded')
    t_max = result.x
    E_max = E(t_max, K, a)
    
    return t_max, E_max

def average_value(K, a, tx):
    """Calcula el valor medio de la función en el intervalo [0,tx]"""
    integral, _ = quad(E, 0, tx, args=(K, a))
    average = integral / tx
    return average

#*=*=*=*=*=*=* Funciones auxiliares de graficación

def esfuerzo_instantaneo(t, a):
    """Calcula el esfuerzo instantáneo sobre un vector numpy t para calibración"""
    return 2 * K_historico * a * t * np.exp(-a * t**2)

def esfuerzo_instantaneo_proyecto(t, K, a):
    """Calcula el esfuerzo instantáneo para un proyecto específico"""
    return 2 * K * a * t * np.exp(-a * t**2)

def esfuerzo_acumulado(t, K, a):
    """Calcula el esfuerzo acumulado sobre un vector numpy t"""
    return K*(1-np.exp(-a * t**2))

def analizar_proyecto(K_proyecto, a_param, nombre="Proyecto", mostrar_detalles=True):
    """Función para analizar un proyecto con parámetros específicos"""
    
    # Parámetros del proyecto
    gamma = 0.9
    tf, Ef = E_proyecto(K_proyecto, a_param, gamma)
    tmax, pmax = find_maximum(K_proyecto, a_param)
    pmed = average_value(K_proyecto, a_param, tf)
    prel = E(tf, K_proyecto, a_param)
    
    if mostrar_detalles:
        print(f"\n=== Análisis del {nombre} (K={K_proyecto} PM, a={a_param:.3f}) ===")
        print(f"Esfuerzo nominal            (K) = {K_proyecto:.1f} PM")
        print(f"Tiempo para entrega        (tf) = {tf:.1f} meses")
        print(f"Esfuerzo acumulado@tf   (E(tf)) = {Ef:.1f} PM")
        print(f"Máxima asignación       (tmax) = {tmax:.1f} meses")
        print(f"Máximo staff asignado  (pmax) = {pmax:.1f} personas")
        print(f"Staff promedio [0,{tf:.1f}]   (pmed) = {pmed:.1f} personas")
        print(f"Staff al release         (prel) = {prel:.1f} personas")
    
    return {
        'K': K_proyecto,
        'a': a_param,
        'tf': tf,
        'Ef': Ef,
        'tmax': tmax,
        'pmax': pmax,
        'pmed': pmed,
        'prel': prel
    }

#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
#*                      Programa principal
#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=

# Datos por defecto
Kp = 212
version = "1.1_modificado"
name = "noname"

os.system('clear')

# Configuración de argumentos
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--version", required=False, help="version", action="store_true")
ap.add_argument("-k", "--esfuerzo", required=False, help="Esfuerzo total")
ap.add_argument("-n", "--name", required=False, help="Nombre proyecto")
ap.add_argument("-a", "--multiplier", required=False, help="Multiplicador para parámetro 'a'", default="1.0")

args = vars(ap.parse_args())

if args['version']:
    print(f"Programa {sys.argv[0]} version {version}")
    sys.exit(0)

if args['name']:
    name = args['name']
else:
    name = 'Proyecto_Analisis'

if args['esfuerzo']:
    Kp = float(args['esfuerzo'])

multiplier_a = float(args['multiplier'])

print(f"=== ANÁLISIS DEL MODELO PNR - {name} ===\n")

#*--- Define el dataset histórico de referencia y calibra
t_data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])        # Tiempo en meses
E_data = np.array([8, 21, 25, 30, 25, 24, 17, 15, 11, 6])  # Esfuerzo instantáneo en persona-mes

# Crear DataFrame para mostrar los datos
df = pd.DataFrame({'Tiempo': t_data, 'Esfuerzo': E_data})
print("Dataset histórico de calibración:")
print(df)

K_historico = np.sum(E_data)
print(f"\nEl esfuerzo total del proyecto histórico es K = {K_historico} PM")

# Calibración del parámetro 'a'
popt, pcov = curve_fit(esfuerzo_instantaneo, t_data, E_data, p0=[0.1])
a_estimada = popt[0]
print(f"Parámetro 'a' estimado por calibración: {a_estimada:.4f}")

# Aplicar multiplicador al parámetro 'a'
a_modificada = a_estimada * multiplier_a
if multiplier_a != 1.0:
    print(f"Parámetro 'a' modificado (x{multiplier_a}): {a_modificada:.4f}")

#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
#*                      PUNTO A: Gráfico comparativo básico
#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=

# Generar curvas para graficación
t_fit = np.linspace(min(t_data), max(t_data), 100)

# Modelo ajustado a datos históricos
E_modelo_historico = esfuerzo_instantaneo(t_fit, a_estimada)

# Proyecto con nuevo esfuerzo usando 'a' calibrada
E_proyecto_nuevo = esfuerzo_instantaneo_proyecto(t_fit, Kp, a_estimada)

# Si se usa 'a' modificada
if multiplier_a != 1.0:
    E_proyecto_modificado = esfuerzo_instantaneo_proyecto(t_fit, Kp, a_modificada)

plt.figure(figsize=(12, 8))
plt.scatter(t_data, E_data, label='Datos históricos observados', color='blue', s=50, zorder=5)
plt.plot(t_fit, E_modelo_historico, label=f'Modelo histórico (K={K_historico} PM)', color='red', linestyle='-', linewidth=2)
plt.plot(t_fit, E_proyecto_nuevo, label=f'Proyecto nuevo (K={Kp} PM, a={a_estimada:.4f})', color='green', linestyle='-', linewidth=2)

if multiplier_a != 1.0:
    plt.plot(t_fit, E_proyecto_modificado, label=f'Proyecto con a modificada (K={Kp} PM, a={a_modificada:.4f})', 
             color='purple', linestyle='--', linewidth=2)

plt.xlabel('Tiempo (meses)', fontsize=12)
plt.ylabel('Esfuerzo instantáneo (personas)', fontsize=12)
plt.title(f'Comparación de Modelos PNR - {name}', fontsize=14)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.show()

#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
#*                      ANÁLISIS DETALLADO
#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=

# Análisis del proyecto histórico
resultado_historico = analizar_proyecto(K_historico, a_estimada, "Proyecto Histórico")

# Análisis del proyecto nuevo
resultado_nuevo = analizar_proyecto(Kp, a_estimada, f"Proyecto Nuevo (K={Kp} PM)")

# Si hay modificación del parámetro 'a'
if multiplier_a != 1.0:
    resultado_modificado = analizar_proyecto(Kp, a_modificada, f"Proyecto con 'a' modificada (x{multiplier_a})")
    
    # Comparación de efectos
    print(f"\n=== COMPARACIÓN DE EFECTOS DEL CAMBIO EN PARÁMETRO 'a' ===")
    print(f"Proyecto original (a={a_estimada:.4f}):")
    print(f"  - Tiempo de entrega: {resultado_nuevo['tf']:.2f} meses")
    print(f"  - Staff máximo: {resultado_nuevo['pmax']:.2f} personas")
    print(f"  - Tiempo del máximo: {resultado_nuevo['tmax']:.2f} meses")
    
    print(f"\nProyecto modificado (a={a_modificada:.4f}):")
    print(f"  - Tiempo de entrega: {resultado_modificado['tf']:.2f} meses")
    print(f"  - Staff máximo: {resultado_modificado['pmax']:.2f} personas")  
    print(f"  - Tiempo del máximo: {resultado_modificado['tmax']:.2f} meses")
    
    # Cálculo de cambios relativos
    cambio_tf = ((resultado_modificado['tf'] - resultado_nuevo['tf']) / resultado_nuevo['tf']) * 100
    cambio_pmax = ((resultado_modificado['pmax'] - resultado_nuevo['pmax']) / resultado_nuevo['pmax']) * 100
    cambio_tmax = ((resultado_modificado['tmax'] - resultado_nuevo['tmax']) / resultado_nuevo['tmax']) * 100
    
    print(f"\nCambios relativos:")
    print(f"  - Tiempo de entrega: {cambio_tf:+.1f}%")
    print(f"  - Staff máximo: {cambio_pmax:+.1f}%")
    print(f"  - Tiempo del máximo: {cambio_tmax:+.1f}%")

#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
#*                      GRÁFICO DE ESFUERZO ACUMULADO
#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=

# Extender el rango temporal para mostrar la curva completa
t_extended = np.linspace(0, max(t_data) * 1.5, 200)

plt.figure(figsize=(12, 6))

# Esfuerzo acumulado para diferentes escenarios
E_acum_historico = esfuerzo_acumulado(t_extended, K_historico, a_estimada)
E_acum_nuevo = esfuerzo_acumulado(t_extended, Kp, a_estimada)

plt.plot(t_extended, E_acum_historico, label=f'Histórico (K={K_historico} PM)', color='red', linewidth=2)
plt.plot(t_extended, E_acum_nuevo, label=f'Proyecto nuevo (K={Kp} PM)', color='green', linewidth=2)

if multiplier_a != 1.0:
    E_acum_modificado = esfuerzo_acumulado(t_extended, Kp, a_modificada)
    plt.plot(t_extended, E_acum_modificado, label=f'Proyecto a modificada (K={Kp} PM, a×{multiplier_a})', 
             color='purple', linestyle='--', linewidth=2)

plt.axhline(y=K_historico, color='red', linestyle=':', alpha=0.7, label=f'K histórico = {K_historico} PM')
plt.axhline(y=Kp, color='green', linestyle=':', alpha=0.7, label=f'K nuevo = {Kp} PM')

plt.xlabel('Tiempo (meses)', fontsize=12)
plt.ylabel('Esfuerzo acumulado (PM)', fontsize=12)
plt.title('Esfuerzo Acumulado vs Tiempo', fontsize=14)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.show()

#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
#*                      ANÁLISIS DE ZONA IMPOSIBLE
#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=

if multiplier_a != 1.0:
    print(f"\n=== ANÁLISIS DE ZONA IMPOSIBLE ===")
    
    # La zona imposible se relaciona con la concentración del esfuerzo
    # Un valor mayor de 'a' concentra más el esfuerzo en menos tiempo
    
    if multiplier_a > 1.0:
        print(f"Con a = {a_modificada:.4f} (x{multiplier_a} del calibrado):")
        print("- El proyecto se concentra más en el tiempo")
        print("- Requiere mayor staff máximo en menos tiempo")
        print("- Puede entrar en 'zona imposible' si el staff requerido excede capacidades organizacionales")
        print("- Mayor riesgo de sobrecarga de recursos")
        
        # Calcular si el staff máximo es extremadamente alto
        if resultado_modificado['pmax'] > resultado_nuevo['pmax'] * 2:
            print("ADVERTENCIA: Staff máximo muy elevado - posible entrada en zona imposible")
        
    else:
        print(f"Con a = {a_modificada:.4f} (x{multiplier_a} del calibrado):")
        print("- El proyecto se extiende más en el tiempo")
        print("- Requiere menor staff máximo distribuido en más tiempo")
        print("- Menor riesgo de zona imposible")
        print("- Mayor duración total del proyecto")

print(f"\n=== FIN DEL ANÁLISIS ===")