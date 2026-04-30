#uzycie: python3 src/emoji_to_pascal.py <input.ep> [output.pas]

from __future__ import annotations

import sys
from pathlib import Path


EMOJI_TO_PASCAL = {
    "🏁": "program",
    "📌": "const",
    "📦": "var",
    "⚙️": "function",
    "🔧": "procedure",
    "🚦": "begin",
    "🛑": "end",
    "↩️": "exit",
    "❓": "if",
    "➡️": "then",
    "🙅": "else",
    "🔁🔂": "repeat",
    "🔂▶️": "until",
    "🔁": "while",
    "▶️": "do",
    "🔂": "for",
    "⬆️": "to",
    "⬇️": "downto",
    "🧭": "case",
    "🧾": "of",
    "🖨️": "writeln",
    "📥": "readln",
    "📤": "var",
    "🔢": "integer",
    "🌊": "real",
    "🧵": "string",
    "✅": "boolean",
    "🔡": "char",
    "📚": "array",
    "🧱": "record",
    "⬅️": ":=",
    "✨": "",
    "➕": "+",
    "➖": "-",
    "✖️": "*",
    "➗": "/",
    "✂️": "mod",
    "🟰": "=",
    "❌": "<>",
    "🔽": "<",
    "⏬": "<=",
    "🔼": ">",
    "⏫": ">=",
    "🤝": "and",
    "🔀": "or",
    "🚫": "not",
    "↔️": "..",
    "💠": ".",
    "🔹": ";",
    "📍": ":",
    "📎": ",",
    "🔚": ".",
    "🤜": "(",
    "🤛": ")",
}

KEYCAP_MAP = {
    "0️⃣": "0",
    "1️⃣": "1",
    "2️⃣": "2",
    "3️⃣": "3",
    "4️⃣": "4",
    "5️⃣": "5",
    "6️⃣": "6",
    "7️⃣": "7",
    "8️⃣": "8",
    "9️⃣": "9",
}


def convert_emoji_numbers(text: str) -> str:
    for keycap, digit in KEYCAP_MAP.items():
        text = text.replace(keycap, digit)
    return text


def convert_emoji_pascal_to_pascal(text: str) -> str:
    text = convert_emoji_numbers(text)
    for emoji in sorted(EMOJI_TO_PASCAL.keys(), key=len, reverse=True):
        text = text.replace(emoji, EMOJI_TO_PASCAL[emoji])
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
