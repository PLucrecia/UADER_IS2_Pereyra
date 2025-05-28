
import json
import os
import sys

class SingletonMeta(type):
    """Metaclase para implementar el patrón Singleton."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class JSONValueFetcher(metaclass=SingletonMeta):
    """Clase Singleton que permite obtener valores desde un archivo JSON."""

    def __init__(self, filename='sitedata.json'):
        self.filename = filename
        self.data = {}
        self._load_json()

    def _load_json(self):
        if not os.path.exists(self.filename):
            raise FileNotFoundError(f"No se encuentra el archivo {self.filename}.")
        with open(self.filename, 'r', encoding='utf-8') as file:
            self.data = json.load(file)

    def get_value(self, key='token1'):
        if key not in self.data:
            raise KeyError(f"La clave '{key}' no existe en {self.filename}.")
        return self.data[key]

if __name__ == "__main__":
    key = sys.argv[1] if len(sys.argv) > 1 else 'token1'
    try:
        fetcher = JSONValueFetcher()
        value = fetcher.get_value(key)
        print(value)
    except Exception as e:
        print(f"Error: {e}")
