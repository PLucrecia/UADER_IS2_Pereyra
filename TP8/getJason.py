
"""
getJason.py - versión orientada a objetos con Singleton

Copyright UADER-FCyT-IS2©2024. Todos los derechos reservados.

Este programa permite obtener valores de claves específicas de un archivo JSON.
"""

import json
import os
import sys

class SingletonMeta(type):
    """Metaclase que asegura que una clase tenga solo una instancia."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class JSONValueFetcher(metaclass=SingletonMeta):
    """
    Clase que carga un archivo JSON y permite recuperar valores por clave.
    """
    def __init__(self, filename='sitedata.json'):
        self.filename = filename
        self.data = {}
        self._load_json()

    def _load_json(self):
        if not os.path.exists(self.filename):
            self._error(f"No se encuentra el archivo '{self.filename}'.")
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
        except json.JSONDecodeError:
            self._error("El archivo JSON está malformado.")

    def get_value(self, key='token1'):
        if key not in self.data:
            self._error(f"La clave '{key}' no existe en el archivo.")
        return self.data[key]

    @staticmethod
    def _error(message):
        print(f"[ERROR]: {message}")
        sys.exit(1)

def main():
    key = sys.argv[1] if len(sys.argv) > 1 else 'token1'
    fetcher = JSONValueFetcher()
    value = fetcher.get_value(key)
    print(value)

if __name__ == "__main__":
    main()
