
import sys
from getJason_b import JSONValueFetcher  # lógica abstracta

def main():
    key = sys.argv[1] if len(sys.argv) > 1 else 'token1'
    try:
        fetcher = JSONValueFetcher()
        value = fetcher.get_value(key)
        print(value)
    except Exception as e:
        print(f"[ERROR]: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()  # Punto de entrada independiente: separación entre UI y lógica
