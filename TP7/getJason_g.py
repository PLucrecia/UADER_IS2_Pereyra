
import sys
from getJason_e import JSONValueFetcher

def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg in ('-v', '--version'):
            print("getJason.py - versión 1.1")
            sys.exit(0)
        elif arg in ('-h', '--help'):
            print("Uso: python getJason.py [clave]\nOpciones: -v versión, -h ayuda")
            sys.exit(0)
        elif arg.startswith('-'):
            print(f"[ERROR]: Opción no reconocida '{arg}'")
            sys.exit(1)
        key = arg
    else:
        key = 'token1'

    try:
        fetcher = JSONValueFetcher()
        value = fetcher.get_value(key)
        print(value)
    except Exception as e:
        print(f"[ERROR]: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
