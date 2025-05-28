
import json
import os
import sys

class JSONValueFetcher:
    """Clase que permite obtener valores desde un archivo JSON."""

    def __init__(self, filename='sitedata.json'):
        self.filename = filename

    def get_value(self, key='token1'):
        """Devuelve el valor de una clave del archivo JSON si existe."""
        if not os.path.exists(self.filename):
            raise FileNotFoundError(f"No se encuentra el archivo {self.filename}.")

        with open(self.filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if key not in data:
            raise KeyError(f"La clave '{key}' no existe en {self.filename}.")

        return data[key]

if __name__ == "__main__":
    key = sys.argv[1] if len(sys.argv) > 1 else 'token1'
    try:
        fetcher = JSONValueFetcher()
        value = fetcher.get_value(key)
        print(value)
    except Exception as e:
        print(f"Error: {e}")
