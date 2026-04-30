#tokenowanie uzycie : python3 src/main.py <plik.ep>
import sys
from pathlib import Path

from lexer import lexer


def main() -> int:
    if len(sys.argv) != 2:
        print("Uzycie: python src/main.py <plik.ep>")
        return 1

    source_path = Path(sys.argv[1])
    if not source_path.exists():
        print(f"Brak pliku: {source_path}")
        return 1

    data = source_path.read_text(encoding="utf-8")
    lexer.input(data)

    try:
        for tok in iter(lexer.token, None):
            print(f"{tok.type:15} {tok.value!r} (linia {tok.lineno})")
    except SyntaxError as exc:
        print(f"Blad leksera: {exc}")
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
