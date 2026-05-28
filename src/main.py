# Tokenizacja: python3 src/main.py <plik.ep>
# Parse AST:     python3 src/main.py --parse <plik.ep>
# Emisja C:      python3 src/main.py --emit-c <plik.ep> [wyjscie.c]
import sys
from pathlib import Path

from lexer import lexer

USAGE = (
    "Uzycie: python3 src/main.py [--parse | --emit-c [wyjscie.c]] <plik.ep>\n"
    "       python3 src/main.py <plik.ep>   # lista tokenow"
)


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


def _parse_cli(argv: list[str]) -> tuple[str, Path | None, Path]:
    """Zwraca (tryb, opcjonalna_sciezka_c, plik_ep)."""
    mode = "tokens"
    output_c: Path | None = None

    if not argv:
        raise ValueError("brak argumentow")

    idx = 0
    if argv[0] == "--parse":
        mode = "parse"
        idx = 1
    elif argv[0] == "--emit-c":
        mode = "emit_c"
        idx = 1
        if idx < len(argv) and argv[idx].endswith(".c"):
            output_c = Path(argv[idx])
            idx += 1

    rest = argv[idx:]
    if len(rest) != 1:
        raise ValueError("wymagany dokladnie jeden plik .ep")

    return mode, output_c, Path(rest[0])


def main() -> int:
    argv = sys.argv[1:]
    if not argv:
        print(USAGE, end="")
        return 1

    try:
        mode, output_c_path, source_path = _parse_cli(argv)
    except ValueError:
        print(USAGE, end="")
        return 1

    if not source_path.exists():
        print(f"Brak pliku: {source_path}")
        return 1

    try:
        data = source_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"Blad odczytu pliku: {exc}", file=sys.stderr)
        return 1

    if mode == "parse":
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

    if mode == "emit_c":
        from parser import parse_source
        from codegen_c import NotImplementedEmit, emit_c
        from semantic import SemanticError, analyze

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

        try:
            analyze(tree)
        except SemanticError as exc:
            print(f"Blad semantyczny: {exc}", file=sys.stderr)
            return 4

        if output_c_path is None:
            output_c_path = Path("output/c") / f"{source_path.stem}.c"

        try:
            c_code = emit_c(tree)
        except NotImplementedEmit as exc:
            print(
                f"Blad emitera C: nieobslugiwany element AST ({exc})",
                file=sys.stderr,
            )
            return 5
        except Exception as exc:
            print(f"Blad emitera C: {exc}", file=sys.stderr)
            return 5

        try:
            output_c_path.parent.mkdir(parents=True, exist_ok=True)
            output_c_path.write_text(c_code, encoding="utf-8")
        except OSError as exc:
            print(f"Blad zapisu pliku C: {exc}", file=sys.stderr)
            return 1
        print(f"Zapisano: {output_c_path}")
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
