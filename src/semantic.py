"""Lekka analiza semantyczna AST EmojiPascal (przed emisją C)."""

from __future__ import annotations


class SemanticError(Exception):
    """Błąd semantyczny (np. niezadeklarowana zmienna)."""


class SymbolTable:
    def __init__(self) -> None:
        self._symbols: dict[str, str] = {}
        self._kinds: dict[str, str] = {}

    def declare(
        self,
        name: str,
        type_token: str,
        *,
        kind: str = "var",
    ) -> None:
        if name in self._symbols:
            raise SemanticError(
                f"Symbol '{name}' zadeklarowany wielokrotnie ({kind})"
            )
        self._symbols[name] = type_token
        self._kinds[name] = kind

    def lookup(self, name: str) -> str:
        if name not in self._symbols:
            raise SemanticError(f"Niezadeklarowana zmienna '{name}'")
        return self._symbols[name]

    def lookup_kind(self, name: str) -> str:
        self.lookup(name)
        return self._kinds[name]


def _type_token(type_node: tuple) -> str:
    if type_node[0] == "TypeSimple":
        return type_node[1]
    if type_node[0] == "TypeArray":
        return "TYPE_ARRAY"
    raise SemanticError(f"Nieobslugiwany typ: {type_node[0]!r}")


def analyze(ast: tuple) -> None:
    """Sprawdza AST programu; przy błędzie rzuca SemanticError."""
    if ast[0] != "Program":
        raise ValueError(f"Oczekiwano Program, jest {ast[0]!r}")
    _Analyzer().visit_block(ast[2])


class _Analyzer:
    def __init__(self) -> None:
        self._subprogram_names: set[str] = set()
        self._subprogram_param_byref: dict[str, list[bool]] = {}

    def _param_byref_sig(self, params: list) -> list[bool]:
        sig: list[bool] = []
        for group in params:
            if group[0] != "Param":
                raise ValueError(f"Oczekiwano Param, jest {group[0]!r}")
            byref, ids, _type_name = group[1], group[2], group[3]
            for _pid in ids:
                sig.append(byref)
        return sig

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
            self._register_subprogram(sub)
        self._visit_compound(table, compound)

    def _register_const(self, table: SymbolTable, node: tuple) -> None:
        if node[0] != "ConstDecl":
            raise ValueError(f"Oczekiwano ConstDecl, jest {node[0]!r}")
        name, value = node[1], node[2]
        table.declare(name, self._literal_type(value), kind="const")

    def _literal_type(self, node: tuple) -> str:
        tag = node[0]
        mapping = {
            "Int": "TYPE_INT",
            "Real": "TYPE_REAL",
            "Bool": "TYPE_BOOL",
            "Str": "TYPE_STRING",
            "Char": "TYPE_CHAR",
        }
        if tag not in mapping:
            raise SemanticError(f"Nieobslugiwana stala: {tag}")
        return mapping[tag]

    def _register_var_decl(self, table: SymbolTable, node: tuple) -> None:
        if node[0] != "VarDecl":
            raise ValueError(f"Oczekiwano VarDecl, jest {node[0]!r}")
        id_list, type_name = node[1], node[2]
        type_token = _type_token(type_name)
        for name in id_list:
            table.declare(name, type_token)

    def _register_subprogram(self, node: tuple) -> None:
        if node[0] == "Procedure":
            name, params, inner = node[1], node[2], node[3]
            if name in self._subprogram_names:
                raise SemanticError(f"Podprogram '{name}' zadeklarowany wielokrotnie")
            self._subprogram_names.add(name)
            self._subprogram_param_byref[name] = self._param_byref_sig(params)
            self._analyze_inner(params, inner)
            return
        if node[0] == "Function":
            name, params, _ret, inner = node[1], node[2], node[3], node[4]
            if name in self._subprogram_names:
                raise SemanticError(f"Podprogram '{name}' zadeklarowany wielokrotnie")
            self._subprogram_names.add(name)
            self._subprogram_param_byref[name] = self._param_byref_sig(params)
            self._analyze_inner(params, inner)
            return
        raise ValueError(f"Nieznany podprogram: {node[0]!r}")

    def _analyze_inner(self, params: list, inner: tuple) -> None:
        table = SymbolTable()
        for group in params:
            if group[0] != "Param":
                raise ValueError(f"Oczekiwano Param, jest {group[0]!r}")
            _byref, ids, type_name = group[1], group[2], group[3]
            type_token = _type_token(type_name)
            for pid in ids:
                table.declare(pid, type_token, kind="param")
        for decl in inner[1]:
            self._register_var_decl(table, decl)
        self._visit_compound(table, inner[2])

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
            self._visit_lvalue(table, node[1])
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
        elif tag == "Repeat":
            for stmt in node[1]:
                self._visit_stmt(table, stmt)
            self._visit_expr(table, node[2])
        elif tag == "Case":
            self._visit_expr(table, node[1])
            for arm in node[2]:
                for label in arm[1]:
                    self._visit_expr(table, label)
                self._visit_stmt(table, arm[2])
            if node[3] is not None:
                self._visit_stmt(table, node[3])
        elif tag == "Return":
            if node[1] is not None:
                self._visit_expr(table, node[1])
        elif tag == "ExprStmt":
            self._visit_call(table, node[1])
        else:
            raise SemanticError(f"Nieobslugiwana instrukcja w analizie: {tag}")

    def _visit_assign(self, table: SymbolTable, node: tuple) -> None:
        self._visit_lvalue(table, node[1])
        self._visit_expr(table, node[2])

    def _visit_for(self, table: SymbolTable, node: tuple) -> None:
        loop_var = node[1]
        if table.lookup(loop_var) != "TYPE_INT":
            raise SemanticError(
                f"Zmienna petli '{loop_var}' musi byc typu integer"
            )
        self._visit_expr(table, node[2])
        self._visit_expr(table, node[3])
        self._visit_stmt(table, node[5])

    def _visit_lvalue(self, table: SymbolTable, node: tuple) -> None:
        if node[0] == "Var":
            table.lookup(node[1])
        elif node[0] == "Index":
            self._visit_lvalue(table, node[1])
            self._visit_expr(table, node[2])
        else:
            raise SemanticError(f"lvalue: {node[0]!r}")

    def _visit_call(self, table: SymbolTable, node: tuple) -> None:
        if node[0] != "Call":
            raise SemanticError(f"Oczekiwano Call, jest {node[0]!r}")
        name = node[1]
        if name not in self._subprogram_names:
            raise SemanticError(f"Nieznany podprogram '{name}'")
        byref_flags = self._subprogram_param_byref.get(name, [])
        for i, arg in enumerate(node[2] or []):
            if i < len(byref_flags) and byref_flags[i]:
                if arg[0] != "Var":
                    raise SemanticError(
                        f"Argument BYREF podprogramu '{name}' musi byc zmienna"
                    )
                table.lookup(arg[1])
            else:
                self._visit_expr(table, arg)

    def _visit_expr(self, table: SymbolTable, node: tuple) -> None:
        tag = node[0]
        if tag == "Var":
            table.lookup(node[1])
        elif tag == "BinOp":
            self._visit_expr(table, node[2])
            self._visit_expr(table, node[3])
        elif tag == "UnaryNot":
            self._visit_expr(table, node[1])
        elif tag == "Call":
            self._visit_call(table, node)
        elif tag == "Index":
            self._visit_lvalue(table, node)
        elif tag == "Cast":
            self._visit_expr(table, node[1])
        elif tag in ("Int", "Real", "Str", "Bool", "Char"):
            pass
        else:
            raise SemanticError(f"Nieobslugiwane wyrazenie: {tag}")
