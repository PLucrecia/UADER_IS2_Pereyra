#!/usr/bin/python
#*-------------------------------------------------------------------------*
#* factorial.py                                                            *
#* calcula el factorial de un número                                       *
#* Dr.P.E.Colla (c) 2022                                                   *
#* Creative commons                                                        *
#*-------------------------------------------------------------------------*
import sys
def factorial(num): 
    if num < 0: 
        print("Factorial de un número negativo no existe")
        return 0
    elif num == 0: 
        return 1
        
    else: 
        fact = 1
        while(num > 1): 
            fact *= num 
            num -= 1
        return fact 
    

def calcular_factoriales(desde, hasta):
    for num in range(desde, hasta + 1):
        print("Factorial", num, "! es", factorial(num))

#Verifica si se paso un argumento en la linea de comandos
if len(sys.argv) == 1:
   #Si no hay argumentos, solicita la entrada manualmente
   rango = input("Ingrese un número o un rango (ej. 4-8, -10, 10-): ")
else:
    #Si hay argumento en la linea de comandos, lo usa
    rango= sys.argv[1]

#Procesa la entrada para determinar si es un numero unico o un rango
if "-" in rango:  # Si es un rango
    if rango.startswith("-"):  # Caso de "-hasta"
        hasta = int(rango[1:])
        desde = 1
    elif rango.endswith("-"):  # Caso de "desde-"
        desde = int(rango[:-1])
        hasta = 60
    else:  # Caso de "desde-hasta"
        desde, hasta = map(int, rango.split("-"))
else:  # Si es un solo número
    desde = hasta = int(rango)

#Llama a la funcion para calcular factoriales en el rango determinado
calcular_factoriales(desde, hasta)