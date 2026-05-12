# Uzycie: python3 src/emoji_to_pascal.py <input.ep> [output.pas]

from __future__ import annotations

import sys
from pathlib import Path

from emoji_language import EMOJI_TO_PASCAL_TEXT, normalize_keycap_digits


def convert_emoji_pascal_to_pascal(text: str) -> str:
    text = normalize_keycap_digits(text)
    for emoji in sorted(EMOJI_TO_PASCAL_TEXT.keys(), key=len, reverse=True):
        text = text.replace(emoji, EMOJI_TO_PASCAL_TEXT[emoji])
    return text


def main() -> int:
    if len(sys.argv) not in (2, 3):
        print("Uzycie: python src/emoji_to_pascal.py <input.ep> [output.pas]")
        return 1

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"Brak pliku wejsciowego: {input_path}")
        return 1

    if len(sys.argv) == 3:
        output_path = Path(sys.argv[2])
    else:
        output_path = Path("output/pascal") / f"{input_path.stem}.pas"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    source = input_path.read_text(encoding="utf-8")
    converted = convert_emoji_pascal_to_pascal(source)
    output_path.write_text(converted, encoding="utf-8")

    print(f"Zapisano: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
