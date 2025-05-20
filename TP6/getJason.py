import json
import sys
import os

#define una funcion que busca una clave dentro de un archivo JSON
def get_value_from_json(key='token1', filename='sitedata.json'):

    #verifica que el archivo JSON exista antes de intentar abrirlo
    if not os.path.exists(filename):
        raise FileNotFoundError(f"No se encuentra el archivo {filename}.")

    #abre el archivo y carga su contenido como un diccionario
    with open(filename, 'r') as file:
        data = json.load(file)

    #verifica que la clave buscada esta dentro del diccionario
    if key not in data:
        raise KeyError(f"La clave '{key}' no existe en {filename}.")

    #devuelve el valor asociado a la clave solicitada
    return data[key]

#este bloque se ejecuta solo si el archivo es ejecutado directamente desde la linea de comandos
if __name__ == "__main__":
    #si se pasa un argumento por consola, se usa como clave; si no se usa "token1" por defecto 
    key = sys.argv[1] if len(sys.argv) > 1 else 'token1'
    try:
        #llama a la funcion para recuperar el valor del JSON y lo guarda en la variable value
        value = get_value_from_json(key)
        #imprime el valor encontrado
        print(value)
    #si ocurre cualquier error, imprime un mensaje para el usuario
    except Exception as e:
        print(f"Error: {e}")