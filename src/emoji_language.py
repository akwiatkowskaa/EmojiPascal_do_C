from __future__ import annotations

from typing import Dict, List, Tuple

# (emoji, TOKEN_PLY, tekst_w_Pascalu_po_zamianie)
EMOJI_DEFINITIONS: List[Tuple[str, str, str]] = [
    # struktura
    ("🏁", "PROGRAM", "program"),
    ("📌", "CONST", "const"),
    ("📐", "TYPE", "type"),
    ("📦", "VAR", "var"),
    ("⚙️", "FUNCTION", "function"),
    ("🔧", "PROCEDURE", "procedure"),
    ("🚦", "BEGIN", "begin"),
    ("🛑", "END", "end"),
    ("↩️", "RETURN", "exit"),
    # sterowanie (dlugie najpierw — kolejnosc sortowania przy budowie regex)
    ("🔁🔂", "REPEAT", "repeat"),
    ("🔂▶️", "UNTIL", "until"),
    ("🔁", "WHILE", "while"),
    ("▶️", "DO", "do"),
    ("🔂", "FOR", "for"),
    ("⬆️", "TO", "to"),
    ("⬇️", "DOWNTO", "downto"),
    ("🧭", "CASE", "case"),
    ("🧾", "OF", "of"),
    ("❓", "IF", "if"),
    ("➡️", "THEN", "then"),
    ("🙅", "ELSE", "else"),
    ("🖨️", "PRINT", "writeln"),
    ("📥", "INPUT", "readln"),
    ("📤", "BYREF", "var"),
    # typy
    ("🔢", "TYPE_INT", "integer"),
    ("🌊", "TYPE_REAL", "real"),
    ("🧵", "TYPE_STRING", "string"),
    ("✅", "TYPE_BOOL", "boolean"),
    ("🔡", "TYPE_CHAR", "char"),
    ("📚", "ARRAY", "array"),
    ("🧱", "RECORD", "record"),
    ("🧺", "SET", "set"),
    ("📥➡️", "IN", "in"),
    ("🗃️", "LBRACKET", "["),
    ("🗄️", "RBRACKET", "]"),
    # operatory
    ("⬅️", "ASSIGN", ":="),
    ("✨", "CAST", ""),
    ("➕", "PLUS", "+"),
    ("➖", "MINUS", "-"),
    ("✖️", "MUL", "*"),
    ("➗", "DIV", "/"),
    ("✂️", "MOD", "mod"),
    ("🟰", "EQ", "="),
    ("❌", "NEQ", "<>"),
    ("🔽", "LT", "<"),
    ("⏬", "LE", "<="),
    ("🔼", "GT", ">"),
    ("⏫", "GE", ">="),
    ("🤝", "AND", "and"),
    ("🔀", "OR", "or"),
    ("🚫", "NOT", "not"),
    ("↔️", "RANGE", ".."),
    ("💠", "FIELD_ACCESS", "."),
    # interpunkcja
    ("🔹", "SEMICOLON", ";"),
    ("📍", "COLON", ":"),
    ("📎", "COMMA", ","),
    ("🔚", "DOT", "."),
    ("🤜", "LPAREN", "("),
    ("🤛", "RPAREN", ")"),
    # literaly logiczne (emoji zamiast true / false)
    ("👍", "LITERAL_BOOL", "true"),
    ("👎", "LITERAL_BOOL", "false"),
]

KEYCAP_MAP: Dict[str, str] = {
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


def _build_maps() -> Tuple[Dict[str, str], Dict[str, str]]:
    to_token: Dict[str, str] = {}
    to_pascal: Dict[str, str] = {}
    for emoji, token, pascal in EMOJI_DEFINITIONS:
        if emoji in to_token and to_token[emoji] != token:
            raise ValueError(f"Konflikt emoji {emoji!r}")
        to_token[emoji] = token
        to_pascal[emoji] = pascal
    return to_token, to_pascal


EMOJI_TO_TOKEN, EMOJI_TO_PASCAL_TEXT = _build_maps()

RESERVED_BOOL_WORDS = {"true": "LITERAL_BOOL", "false": "LITERAL_BOOL"}


def emoji_regex_pattern() -> str:
    """Regula PLY: najdluzsze dopasowanie najpierw."""
    import re

    keys = sorted(EMOJI_TO_TOKEN.keys(), key=len, reverse=True)
    return "|".join(re.escape(k) for k in keys)


def normalize_keycap_digits(text: str) -> str:
    for keycap, digit in KEYCAP_MAP.items():
        text = text.replace(keycap, digit)
    return text
