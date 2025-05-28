# getJason_c.py

import sys
from getJason_b import JSONValueFetcher  # Reutiliza la versión Singleton

def main():
    if len(sys.argv) > 1:
        key = sys.argv[1]
        if key.startswith('-'):
            print(f"[ERROR]: Opción no válida: '{key}'")
            sys.exit(1)
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
