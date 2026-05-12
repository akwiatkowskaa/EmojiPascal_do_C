# Tokenizacja: python3 src/main.py <plik.ep>
# Parse AST:     python3 src/main.py --parse <plik.ep>
import sys
from pathlib import Path

from lexer import lexer


def simple_dump(node, indent=0):
    """Czytelny druk tuple-AST (jak repr z wcięciami)."""
    pad = "  " * indent
    if isinstance(node, tuple):
        head = node[0]
        print(f"{pad}{head}")
        for part in node[1:]:
            simple_dump(part, indent + 1)
    elif isinstance(node, list):
        print(f"{pad}[")
        for item in node:
            simple_dump(item, indent + 1)
        print(f"{pad}]")
    else:
        print(f"{pad}{node!r}")


def main() -> int:
    argv = sys.argv[1:]
    if not argv:
        print("Uzycie: python3 src/main.py [--parse] <plik.ep>")
        return 1

    do_parse = False
    if argv[0] == "--parse":
        do_parse = True
        argv = argv[1:]

    if len(argv) != 1:
        print("Uzycie: python3 src/main.py [--parse] <plik.ep>")
        return 1

    source_path = Path(argv[0])
    if not source_path.exists():
        print(f"Brak pliku: {source_path}")
        return 1

    data = source_path.read_text(encoding="utf-8")

    if do_parse:
        from parser import parse_source

        try:
            tree = parse_source(data)
        except SyntaxError as exc:
            print(f"Blad skladni: {exc}")
            return 3
        except Exception as exc:
            print(f"Blad parsera: {exc}")
            return 3
        if tree is None:
            print("Blad parsera: pusty wynik")
            return 3
        print("=== AST (tuple) ===")
        simple_dump(tree)
        return 0

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
