"""Lekka analiza semantyczna AST EmojiPascal (przed emisją C)."""

from __future__ import annotations


class SemanticError(Exception):
    """Błąd semantyczny (np. niezadeklarowana zmienna)."""


class SymbolTable:
    def __init__(self) -> None:
        self._symbols: dict[str, str] = {}

    def declare(self, name: str, type_token: str, *, kind: str = "var") -> None:
        if name in self._symbols:
            raise SemanticError(
                f"Symbol '{name}' zadeklarowany wielokrotnie ({kind})"
            )
        self._symbols[name] = type_token

    def lookup(self, name: str) -> str:
        if name not in self._symbols:
            raise SemanticError(f"Niezadeklarowana zmienna '{name}'")
        return self._symbols[name]

    def has(self, name: str) -> bool:
        return name in self._symbols


def _type_token(type_node: tuple) -> str:
    if type_node[0] == "TypeSimple":
        return type_node[1]
    raise SemanticError(f"Nieobslugiwany typ: {type_node[0]!r}")


def analyze(ast: tuple) -> None:
    """Sprawdza AST programu; przy błędzie rzuca SemanticError."""
    if ast[0] != "Program":
        raise ValueError(f"Oczekiwano Program, jest {ast[0]!r}")
    _Analyzer().visit_block(ast[2])


class _Analyzer:
    def visit_block(self, node: tuple) -> None:
        if node[0] != "Block":
            raise ValueError(f"Oczekiwano Block, jest {node[0]!r}")
        const_section, var_section, subprograms, compound = (
            node[1],
            node[2],
            node[3],
            node[4],
        )
        table = SymbolTable()
        for decl in const_section:
            self._register_const(table, decl)
        for decl in var_section:
            self._register_var_decl(table, decl)
        for sub in subprograms:
            self._check_subprogram(sub)
        self._visit_compound(table, compound)

    def _register_const(self, table: SymbolTable, node: tuple) -> None:
        if node[0] != "ConstDecl":
            raise ValueError(f"Oczekiwano ConstDecl, jest {node[0]!r}")
        name, value = node[1], node[2]
        type_token = self._literal_type(value)
        table.declare(name, type_token, kind="const")

    def _literal_type(self, node: tuple) -> str:
        tag = node[0]
        if tag == "Int":
            return "TYPE_INT"
        if tag == "Real":
            return "TYPE_REAL"
        if tag == "Bool":
            return "TYPE_BOOL"
        if tag == "Str":
            return "TYPE_STRING"
        if tag == "Char":
            return "TYPE_CHAR"
        raise SemanticError(f"Nieobslugiwana stala: {tag}")

    def _register_var_decl(self, table: SymbolTable, node: tuple) -> None:
        if node[0] != "VarDecl":
            raise ValueError(f"Oczekiwano VarDecl, jest {node[0]!r}")
        id_list, type_name = node[1], node[2]
        type_token = _type_token(type_name)
        for name in id_list:
            table.declare(name, type_token)

    def _check_subprogram(self, node: tuple) -> None:
        """Podprogramy — pełna semantyka w fazie F; na razie tylko składnia w AST."""
        tag = node[0]
        if tag not in ("Procedure", "Function"):
            raise ValueError(f"Nieznany podprogram: {tag}")

    def _visit_compound(self, table: SymbolTable, node: tuple) -> None:
        if node[0] != "Compound":
            raise ValueError(f"Oczekiwano Compound, jest {node[0]!r}")
        for stmt in node[1]:
            self._visit_stmt(table, stmt)

    def _visit_stmt(self, table: SymbolTable, node: tuple) -> None:
        tag = node[0]
        if tag == "Assign":
            self._visit_assign(table, node)
        elif tag == "Compound":
            self._visit_compound(table, node)
        elif tag == "Print":
            for expr in node[1] or []:
                self._visit_expr(table, expr)
        elif tag == "Input":
            self._visit_var_ref(table, node[1])
        elif tag == "For":
            self._visit_for(table, node)
        elif tag == "While":
            self._visit_expr(table, node[1])
            self._visit_stmt(table, node[2])
        elif tag == "If":
            self._visit_expr(table, node[1])
            self._visit_stmt(table, node[2])
            if node[3] is not None:
                self._visit_stmt(table, node[3])
        else:
            raise SemanticError(f"Nieobslugiwana instrukcja w analizie: {tag}")

    def _visit_assign(self, table: SymbolTable, node: tuple) -> None:
        lhs, rhs = node[1], node[2]
        self._visit_var_ref(table, lhs)
        self._visit_expr(table, rhs)

    def _visit_for(self, table: SymbolTable, node: tuple) -> None:
        loop_var = node[1]
        loop_type = table.lookup(loop_var)
        if loop_type != "TYPE_INT":
            raise SemanticError(
                f"Zmienna petli '{loop_var}' musi byc typu integer (jest {loop_type})"
            )
        self._visit_expr(table, node[2])
        self._visit_expr(table, node[3])
        self._visit_stmt(table, node[5])

    def _visit_var_ref(self, table: SymbolTable, node: tuple) -> None:
        if node[0] != "Var":
            raise SemanticError(f"Oczekiwano Var, jest {node[0]!r}")
        table.lookup(node[1])

    def _visit_expr(self, table: SymbolTable, node: tuple) -> None:
        tag = node[0]
        if tag == "Var":
            table.lookup(node[1])
        elif tag == "BinOp":
            self._visit_expr(table, node[2])
            self._visit_expr(table, node[3])
        elif tag in ("Int", "Real", "Str", "Bool", "Char"):
            pass
        else:
            raise SemanticError(f"Nieobslugiwane wyrazenie: {tag}")
