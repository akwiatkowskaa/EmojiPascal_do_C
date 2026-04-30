import re
from typing import Dict

import ply.lex as lex

_KEYCAP_MAP = {
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


reserved_map: Dict[str, str] = {
    "true": "LITERAL_BOOL",
    "false": "LITERAL_BOOL",
}

emoji_map: Dict[str, str] = {
    "🏁": "PROGRAM",
    "📌": "CONST",
    "📦": "VAR",
    "⚙️": "FUNCTION",
    "🔧": "PROCEDURE",
    "🚦": "BEGIN",
    "🛑": "END",
    "↩️": "RETURN",
    "❓": "IF",
    "➡️": "THEN",
    "🙅": "ELSE",
    "🔁": "WHILE",
    "▶️": "DO",
    "🔁🔂": "REPEAT",
    "🔂▶️": "UNTIL",
    "🔂": "FOR",
    "⬆️": "TO",
    "⬇️": "DOWNTO",
    "🧭": "CASE",
    "🧾": "OF",
    "🖨️": "PRINT",
    "📥": "INPUT",
    "📤": "BYREF",
    "🔢": "TYPE_INT",
    "🌊": "TYPE_REAL",
    "🧵": "TYPE_STRING",
    "✅": "TYPE_BOOL",
    "🔡": "TYPE_CHAR",
    "📚": "ARRAY",
    "🧱": "RECORD",
    "⬅️": "ASSIGN",
    "✨": "CAST",
    "➕": "PLUS",
    "➖": "MINUS",
    "✖️": "MUL",
    "➗": "DIV",
    "✂️": "MOD",
    "🟰": "EQ",
    "❌": "NEQ",
    "🔽": "LT",
    "⏬": "LE",
    "🔼": "GT",
    "⏫": "GE",
    "🤝": "AND",
    "🔀": "OR",
    "🚫": "NOT",
    "↔️": "RANGE",
    "💠": "FIELD_ACCESS",
    "🔹": "SEMICOLON",
    "📍": "COLON",
    "📎": "COMMA",
    "🔚": "DOT",
    "🤜": "LPAREN",
    "🤛": "RPAREN",
}

tokens = [
    # keywords / control
    "PROGRAM",
    "CONST",
    "VAR",
    "FUNCTION",
    "PROCEDURE",
    "BEGIN",
    "END",
    "RETURN",
    "IF",
    "THEN",
    "ELSE",
    "WHILE",
    "DO",
    "REPEAT",
    "UNTIL",
    "FOR",
    "TO",
    "DOWNTO",
    "CASE",
    "OF",
    "PRINT",
    "INPUT",
    "BYREF",
    # types
    "TYPE_INT",
    "TYPE_REAL",
    "TYPE_STRING",
    "TYPE_BOOL",
    "TYPE_CHAR",
    "ARRAY",
    "RECORD",
    # operators
    "ASSIGN",
    "CAST",
    "PLUS",
    "MINUS",
    "MUL",
    "DIV",
    "MOD",
    "EQ",
    "NEQ",
    "LT",
    "LE",
    "GT",
    "GE",
    "AND",
    "OR",
    "NOT",
    "RANGE",
    "FIELD_ACCESS",
    # punctuation
    "SEMICOLON",
    "COLON",
    "COMMA",
    "DOT",
    "LPAREN",
    "RPAREN",
    # literals / identifiers
    "IDENTIFIER",
    "LITERAL_INT",
    "LITERAL_REAL",
    "LITERAL_STR",
    "LITERAL_CHAR",
    "LITERAL_BOOL",
]

t_ignore = " \t\r"


def t_COMMENT(t):
    r"(//[^\n]*|\{[^}]*\}|\(\*[\s\S]*?\*\))"
    pass


def t_LITERAL_REAL(t):
    r"(?:[0-9]\ufe0f?\u20e3|[0-9])+(?:\.(?:[0-9]\ufe0f?\u20e3|[0-9])+)"
    for keycap, digit in _KEYCAP_MAP.items():
        t.value = t.value.replace(keycap, digit)
    return t


def t_LITERAL_INT(t):
    r"(?:[0-9]\ufe0f?\u20e3|[0-9])+"
    for keycap, digit in _KEYCAP_MAP.items():
        t.value = t.value.replace(keycap, digit)
    return t


def t_LITERAL_STR(t):
    r'"([^"\\]|\\.)*"'
    return t


def t_LITERAL_CHAR(t):
    r"'([^'\\]|\\.)'"
    return t


def t_IDENTIFIER(t):
    r"[A-Za-z_][A-Za-z0-9_]*"
    lower = t.value.lower()
    if lower in reserved_map:
        t.type = reserved_map[lower]
    return t


def t_EMOJI_TOKEN(t):
    t.type = emoji_map[t.value]
    return t


t_EMOJI_TOKEN.__doc__ = "|".join(re.escape(k) for k in sorted(emoji_map.keys(), key=len, reverse=True))


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_error(t):
    raise SyntaxError(f"Nieznany znak: {t.value[0]!r} (linia {t.lexer.lineno})")


lexer = lex.lex(reflags=re.UNICODE)

