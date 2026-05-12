import re

import ply.lex as lex

from emoji_language import (
    EMOJI_TO_PASCAL_TEXT,
    EMOJI_TO_TOKEN,
    RESERVED_BOOL_WORDS,
    emoji_regex_pattern,
    normalize_keycap_digits,
)

tokens = [
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
    "TYPE_INT",
    "TYPE_REAL",
    "TYPE_STRING",
    "TYPE_BOOL",
    "TYPE_CHAR",
    "ARRAY",
    "RECORD",
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
    "SEMICOLON",
    "COLON",
    "COMMA",
    "DOT",
    "LPAREN",
    "RPAREN",
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
    t.value = normalize_keycap_digits(t.value)
    return t


def t_LITERAL_INT(t):
    r"(?:[0-9]\ufe0f?\u20e3|[0-9])+"
    t.value = normalize_keycap_digits(t.value)
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
    if lower in RESERVED_BOOL_WORDS:
        t.type = RESERVED_BOOL_WORDS[lower]
    return t


def t_EMOJI_TOKEN(t):
    t.type = EMOJI_TO_TOKEN[t.value]
    if t.type == "LITERAL_BOOL":
        t.value = EMOJI_TO_PASCAL_TEXT[t.value]
    return t


t_EMOJI_TOKEN.__doc__ = emoji_regex_pattern()


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_error(t):
    raise SyntaxError(f"Nieznany znak: {t.value[0]!r} (linia {t.lexer.lineno})")


lexer = lex.lex(reflags=re.UNICODE)
