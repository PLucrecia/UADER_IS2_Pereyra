

import sys
from getJason_e import JSONValueFetcher

def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg.startswith('-') and arg not in ('-v', '--version', '-h', '--help'):
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
