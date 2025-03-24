#!/usr/bin/python
#*-------------------------------------------------------------------------*
#* factorial_OOP.py                                                         *
#* Calcula el factorial de un número usando Programación Orientada a Objetos *
#* Basado en factorial.py                                                   *
#*-------------------------------------------------------------------------*

import sys

class Factorial:
    
    def __init__(self, min, max):
        self.min = min
        self.max = max
    
    def calcular(self, num):
        if num < 0:
            print("Factorial de un número negativo no existe")
            return 0
        elif num == 0:
            return 1
        else:
            fact = 1
            while num > 1:
                fact *= num
                num -= 1
            return fact
    
    def run(self):
        for num in range(self.min, self.max + 1):
            print(f"Factorial {num}! es {self.calcular(num)}")

if len(sys.argv) == 3:
    min_value = int(sys.argv[1])
    max_value = int(sys.argv[2])
else:
    min_value = int(input("Ingrese el valor mínimo: "))
    max_value = int(input("Ingrese el valor máximo: "))

factorial_obj = Factorial(min_value, max_value)
factorial_obj.run()