"""Lekka analiza semantyczna AST EmojiPascal (przed emisją C)."""

from __future__ import annotations

MAX_ENUM_MEMBERS = 32


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
    if type_node[0] == "TypeRecord":
        return "TYPE_RECORD"
    if type_node[0] == "TypeNamed":
        return f"ENUM:{type_node[1]}"
    if type_node[0] == "TypeSet":
        return f"SET:{type_node[1]}"
    raise SemanticError(f"Nieobslugiwany typ: {type_node[0]!r}")


def _record_field_map(type_node: tuple) -> dict[str, str]:
    if type_node[0] != "TypeRecord":
        raise ValueError(f"Oczekiwano TypeRecord, jest {type_node[0]!r}")
    fields: dict[str, str] = {}
    for field in type_node[1]:
        if field[0] != "RecordField":
            raise ValueError(f"Oczekiwano RecordField, jest {field[0]!r}")
        ids, ftype = field[1], field[2]
        if ftype[0] != "TypeSimple":
            raise SemanticError(
                f"Pole rekordu: nieobslugiwany typ {ftype[0]!r}"
            )
        type_token = ftype[1]
        for fid in ids:
            if fid in fields:
                raise SemanticError(
                    f"Pole '{fid}' zadeklarowane wielokrotnie w rekordzie"
                )
            fields[fid] = type_token
    return fields


def analyze(ast: tuple) -> None:
    """Sprawdza AST programu; przy błędzie rzuca SemanticError."""
    if ast[0] != "Program":
        raise ValueError(f"Oczekiwano Program, jest {ast[0]!r}")
    _Analyzer().visit_block(ast[2])


class _Analyzer:
    def __init__(self) -> None:
        self._subprogram_names: set[str] = set()
        self._subprogram_param_byref: dict[str, list[bool]] = {}
        self._function_return_types: dict[str, str] = {}
        self._record_fields: dict[str, dict[str, str]] = {}
        self._enum_types: dict[str, list[str]] = {}
        self._enum_member_of: dict[str, str] = {}
        self._set_var_enum: dict[str, str] = {}

    def _param_byref_sig(self, params: list) -> list[bool]:
        sig: list[bool] = []
        for group in params:
            if group[0] != "Param":
                raise ValueError(f"Oczekiwano Param, jest {group[0]!r}")
            byref, ids, _type_name = group[1], group[2], group[3]
            for _pid in ids:
                sig.append(byref)
        return sig

    def _lookup_name(self, table: SymbolTable, name: str) -> str:
        if name in self._enum_member_of:
            return f"ENUMVAL:{self._enum_member_of[name]}"
        return table.lookup(name)

    def _enum_name_from_type(self, type_token: str) -> str | None:
        if type_token.startswith("ENUM:"):
            return type_token[5:]
        if type_token.startswith("SET:"):
            return type_token[4:]
        if type_token.startswith("ENUMVAL:"):
            return type_token[8:]
        return None

    def _register_type_decl(self, table: SymbolTable, node: tuple) -> None:
        if node[0] != "TypeEnumDecl":
            raise ValueError(f"Oczekiwano TypeEnumDecl, jest {node[0]!r}")
        enum_name, members = node[1], node[2]
        if enum_name in self._enum_types:
            raise SemanticError(f"Typ wyliczeniowy '{enum_name}' zadeklarowany wielokrotnie")
        if not members:
            raise SemanticError(f"Typ wyliczeniowy '{enum_name}' musi miec co najmniej jeden element")
        if len(members) > MAX_ENUM_MEMBERS:
            raise SemanticError(
                f"Typ wyliczeniowy '{enum_name}' moze miec maksymalnie {MAX_ENUM_MEMBERS} elementow"
            )
        if len(members) != len(set(members)):
            raise SemanticError(f"Typ wyliczeniowy '{enum_name}' ma powtarzajace sie elementy")
        self._enum_types[enum_name] = list(members)
        table.declare(enum_name, f"ENUMTYPE:{enum_name}", kind="type")
        for member in members:
            if member in self._enum_member_of:
                raise SemanticError(
                    f"Element wyliczeniowy '{member}' zadeklarowany wielokrotnie"
                )
            self._enum_member_of[member] = enum_name
            table.declare(member, f"ENUMVAL:{enum_name}", kind="enum_member")

    def visit_block(self, node: tuple) -> None:
        if node[0] != "Block":
            raise ValueError(f"Oczekiwano Block, jest {node[0]!r}")
        const_section, type_section, var_section, subprograms, compound = (
            node[1],
            node[2],
            node[3],
            node[4],
            node[5],
        )
        table = SymbolTable()
        for decl in const_section:
            self._register_const(table, decl)
        for decl in type_section:
            self._register_type_decl(table, decl)
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
        if type_name[0] == "TypeNamed":
            enum_name = type_name[1]
            if enum_name not in self._enum_types:
                raise SemanticError(f"Nieznany typ wyliczeniowy '{enum_name}'")
        if type_name[0] == "TypeSet":
            enum_name = type_name[1]
            if enum_name not in self._enum_types:
                raise SemanticError(
                    f"Zbior: nieznany typ wyliczeniowy '{enum_name}'"
                )
        type_token = _type_token(type_name)
        field_map = (
            _record_field_map(type_name)
            if type_name[0] == "TypeRecord"
            else None
        )
        for name in id_list:
            table.declare(name, type_token)
            if field_map is not None:
                self._record_fields[name] = dict(field_map)
            if type_name[0] == "TypeSet":
                self._set_var_enum[name] = type_name[1]

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
            name, params, ret_type, inner = node[1], node[2], node[3], node[4]
            if name in self._subprogram_names:
                raise SemanticError(f"Podprogram '{name}' zadeklarowany wielokrotnie")
            self._subprogram_names.add(name)
            self._subprogram_param_byref[name] = self._param_byref_sig(params)
            self._function_return_types[name] = _type_token(ret_type)
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
        lhs_type = self._lvalue_type(table, node[1])
        self._visit_expr(table, node[2], expected_type=lhs_type)

    def _visit_for(self, table: SymbolTable, node: tuple) -> None:
        loop_var = node[1]
        if table.lookup(loop_var) != "TYPE_INT":
            raise SemanticError(
                f"Zmienna petli '{loop_var}' musi byc typu integer"
            )
        self._visit_expr(table, node[2])
        self._visit_expr(table, node[3])
        self._visit_stmt(table, node[5])

    def _lvalue_type(self, table: SymbolTable, node: tuple) -> str | None:
        if node[0] == "Var":
            return self._lookup_name(table, node[1])
        if node[0] == "Field":
            base, field = node[1], node[2]
            if base[0] != "Var":
                raise SemanticError("Dostep do pola tylko przez zmienna rekordowa")
            var = base[1]
            if table.lookup(var) != "TYPE_RECORD":
                raise SemanticError(
                    f"Zmienna '{var}' nie jest rekordem (dostep do pola '{field}')"
                )
            if field not in self._record_fields.get(var, {}):
                raise SemanticError(
                    f"Rekord '{var}' nie ma pola '{field}'"
                )
            return self._record_fields[var][field]
        if node[0] == "Index":
            self._lvalue_type(table, node[1])
            self._visit_expr(table, node[2])
            return "TYPE_INT"
        raise SemanticError(f"lvalue: {node[0]!r}")

    def _visit_lvalue(self, table: SymbolTable, node: tuple) -> None:
        self._lvalue_type(table, node)

    def _expr_type(self, table: SymbolTable, node: tuple) -> str:
        tag = node[0]
        if tag == "Var":
            return self._lookup_name(table, node[1])
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
        if tag == "SetLit":
            return self._set_lit_type(table, node[1])
        if tag == "In":
            self._visit_in(table, node)
            return "TYPE_BOOL"
        if tag == "BinOp":
            return self._binop_type(table, node)
        if tag == "UnaryNot":
            self._visit_expr(table, node[1])
            return "TYPE_BOOL"
        if tag == "Call":
            self._visit_call(table, node)
            name = node[1]
            return self._function_return_types.get(name, "TYPE_INT")
        if tag == "Index":
            self._visit_lvalue(table, node)
            return "TYPE_INT"
        if tag == "Cast":
            self._visit_expr(table, node[1])
            return _type_token(node[2]) if node[2][0] == "TypeSimple" else "TYPE_INT"
        if tag == "Field":
            return self._lvalue_type(table, node) or "TYPE_INT"
        raise SemanticError(f"Nieobslugiwane wyrazenie: {tag}")

    def _set_lit_type(self, table: SymbolTable, members: list[str]) -> str:
        if not members:
            return "SET:__EMPTY__"
        enum_name: str | None = None
        for member in members:
            if member not in self._enum_member_of:
                raise SemanticError(
                    f"Literał zbioru: nieznany element wyliczeniowy '{member}'"
                )
            member_enum = self._enum_member_of[member]
            if enum_name is None:
                enum_name = member_enum
            elif member_enum != enum_name:
                raise SemanticError("Literał zbioru: elementy z roznych typow wyliczeniowych")
        return f"SET:{enum_name}"

    def _binop_type(self, table: SymbolTable, node: tuple) -> str:
        op, left, right = node[1], node[2], node[3]
        left_type = self._expr_type(table, left)
        right_type = self._expr_type(table, right)
        if op in ("PLUS", "MINUS", "MUL"):
            if left_type.startswith("SET:") and right_type.startswith("SET:"):
                if left_type != right_type:
                    raise SemanticError("Operacje na zbiorach wymagaja tego samego typu")
                return left_type
        if op in ("LE", "GE"):
            if left_type.startswith("SET:") and right_type.startswith("SET:"):
                if left_type != right_type:
                    raise SemanticError("Porownanie zbiorow wymaga tego samego typu")
                return "TYPE_BOOL"
        if op in ("EQ", "NEQ"):
            if left_type.startswith("SET:") and right_type.startswith("SET:"):
                if left_type != right_type:
                    raise SemanticError("Porownanie zbiorow wymaga tego samego typu")
                return "TYPE_BOOL"
        if op in ("AND", "OR"):
            return "TYPE_BOOL"
        if op in ("PLUS", "MINUS", "MUL", "DIV"):
            if left_type == "TYPE_REAL" or right_type == "TYPE_REAL":
                return "TYPE_REAL"
        if op == "MOD":
            return "TYPE_INT"
        return "TYPE_INT"

    def _visit_in(self, table: SymbolTable, node: tuple) -> None:
        left_type = self._expr_type(table, node[1])
        right_type = self._expr_type(table, node[2])
        left_enum = self._enum_name_from_type(left_type)
        if left_enum is None:
            raise SemanticError("Operator IN: lewa strona musi byc elementem lub zmienna wyliczeniowa")
        if not right_type.startswith("SET:"):
            raise SemanticError("Operator IN: prawa strona musi byc zbiorem")
        right_enum = right_type[4:]
        if right_enum == "__EMPTY__":
            raise SemanticError("Operator IN: nie mozna sprawdzac przynaleznosci do pustego literału bez kontekstu")
        if left_enum != right_enum:
            raise SemanticError("Operator IN: element i zbior musza pochodzic z tego samego typu wyliczeniowego")

    def _visit_expr(
        self,
        table: SymbolTable,
        node: tuple,
        *,
        expected_type: str | None = None,
    ) -> None:
        expr_type = self._expr_type(table, node)
        if expected_type is None:
            return
        if expected_type.startswith("SET:") and expr_type == "SET:__EMPTY__":
            enum_name = expected_type[4:]
            if enum_name not in self._enum_types:
                raise SemanticError("Przypisanie do zbioru: nieznany typ wyliczeniowy")
            return
        if expected_type != expr_type:
            if (
                expected_type.startswith("SET:")
                and expr_type.startswith("SET:")
                and expected_type == expr_type
            ):
                return
            if (
                expected_type.startswith("ENUM:")
                and expr_type.startswith("ENUMVAL:")
                and expected_type[5:] == expr_type[8:]
            ):
                return
            raise SemanticError(
                f"Niezgodnosc typow: oczekiwano {expected_type}, jest {expr_type}"
            )

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
