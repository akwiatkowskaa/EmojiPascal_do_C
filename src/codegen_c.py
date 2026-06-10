"""Emiter kodu C z drzewa AST EmojiPascal (tuple z parser.py)."""

from __future__ import annotations


class NotImplementedEmit(NotImplementedError):
    """Brak emisji dla węzła AST — kolejna faza planu."""


class EmitContext:
    def __init__(self) -> None:
        self.lines: list[str] = []
        self.indent_level = 0
        self.array_bounds: dict[str, tuple[int, int]] = {}
        self.var_types: dict[str, str] = {}

    def emit_line(self, text: str) -> None:
        pad = "    " * self.indent_level
        self.lines.append(f"{pad}{text}")

    def indent(self) -> None:
        self.indent_level += 1

    def dedent(self) -> None:
        self.indent_level -= 1

    def render(self) -> str:
        return "\n".join(self.lines) + "\n"

    def emit_program(self, node: tuple) -> None:
        if node[0] != "Program":
            raise ValueError(f"Oczekiwano Program, jest {node[0]!r}")
        program_name, block = node[1], node[2]
        self.emit_line("#include <stdio.h>")
        self.emit_line("")
        self.emit_line(f"/* Program: {program_name} */")

        const_section, var_section, subprograms, compound = (
            block[1],
            block[2],
            block[3],
            block[4],
        )
        for decl in const_section:
            self.emit_const_decl(decl)
        if const_section:
            self.emit_line("")

        for sub in subprograms:
            self.emit_subprogram(sub)
        if subprograms:
            self.emit_line("")

        self.emit_line("int main(void) {")
        self.indent()
        for var_decl in var_section:
            self.emit_var_decl(var_decl)
        if var_section and compound[1]:
            self.emit_line("")
        self.emit_compound(compound)
        self.emit_line("return 0;")
        self.dedent()
        self.emit_line("}")

    def emit_const_decl(self, node: tuple) -> None:
        if node[0] != "ConstDecl":
            raise ValueError(f"Oczekiwano ConstDecl, jest {node[0]!r}")
        name, value = node[1], node[2]
        self.emit_line(f"#define {name} {self.emit_expr(value)}")

    def emit_subprogram(self, node: tuple) -> None:
        saved_bounds = self.array_bounds.copy()
        saved_types = self.var_types.copy()
        try:
            if node[0] == "Procedure":
                name, params, inner = node[1], node[2], node[3]
                self.emit_line(f"void {name}({self.emit_params(params)}) {{")
                self.indent()
                self.emit_inner_block(inner)
                self.dedent()
                self.emit_line("}")
                return
            if node[0] == "Function":
                name, params, ret_type, inner = node[1], node[2], node[3], node[4]
                c_ret = self.type_to_c(ret_type)
                self.emit_line(f"{c_ret} {name}({self.emit_params(params)}) {{")
                self.indent()
                self.emit_inner_block(inner)
                self.dedent()
                self.emit_line("}")
                return
            raise ValueError(f"Nieznany podprogram: {node[0]!r}")
        finally:
            self.array_bounds = saved_bounds
            self.var_types = saved_types

    def emit_params(self, params: list) -> str:
        if not params:
            return "void"
        parts: list[str] = []
        for group in params:
            if group[0] != "Param":
                raise NotImplementedEmit(f"param: {group[0]!r}")
            byref, ids, type_name = group[1], group[2], group[3]
            if byref:
                raise NotImplementedEmit("parametru var (BYREF)")
            c_type = self.type_to_c(type_name)
            for pid in ids:
                self.var_types[pid] = c_type
                parts.append(f"{c_type} {pid}")
        return ", ".join(parts)

    def emit_inner_block(self, node: tuple) -> None:
        if node[0] != "InnerBlock":
            raise ValueError(f"Oczekiwano InnerBlock, jest {node[0]!r}")
        var_section, compound = node[1], node[2]
        saved_bounds = self.array_bounds.copy()
        saved_types = self.var_types.copy()
        for var_decl in var_section:
            self.emit_var_decl(var_decl)
        if var_section and compound[1]:
            self.emit_line("")
        self.emit_compound(compound)
        self.array_bounds = saved_bounds
        self.var_types = saved_types

    def emit_var_decl(self, node: tuple) -> None:
        if node[0] != "VarDecl":
            raise ValueError(f"Oczekiwano VarDecl, jest {node[0]!r}")
        id_list, type_name = node[1], node[2]
        if type_name[0] == "TypeArray":
            low = int(type_name[1][1])
            high = int(type_name[2][1])
            size = high - low + 1
            elem = self.type_to_c(("TypeSimple", type_name[3]))
            for name in id_list:
                self.array_bounds[name] = (low, high)
                self.var_types[name] = f"{elem}[]"
                self.emit_line(f"{elem} {name}[{size}];")
            return
        c_type = self.type_to_c(type_name)
        for name in id_list:
            self.var_types[name] = c_type
        names = ", ".join(id_list)
        self.emit_line(f"{c_type} {names};")

    def type_to_c(self, type_node: tuple) -> str:
        if type_node[0] != "TypeSimple":
            raise NotImplementedEmit(f"typ: {type_node[0]!r}")
        mapping = {
            "TYPE_INT": "int",
            "TYPE_BOOL": "int",
            "TYPE_STRING": "char*",
            "TYPE_REAL": "double",
            "TYPE_CHAR": "char",
        }
        token = type_node[1]
        if token not in mapping:
            raise NotImplementedEmit(f"typ: {token}")
        return mapping[token]

    def emit_compound(self, node: tuple) -> None:
        if node[0] != "Compound":
            raise ValueError(f"Oczekiwano Compound, jest {node[0]!r}")
        for stmt in node[1]:
            self.emit_stmt(stmt)

    def emit_stmt(self, node: tuple) -> None:
        tag = node[0]
        handlers = {
            "Assign": self.emit_assign,
            "Compound": self.emit_compound,
            "Print": self.emit_print,
            "Input": self.emit_input,
            "For": self.emit_for,
            "While": self.emit_while,
            "If": self.emit_if,
            "Repeat": self.emit_repeat,
            "Case": self.emit_case,
            "Return": self.emit_return,
            "ExprStmt": self.emit_expr_stmt,
        }
        fn = handlers.get(tag)
        if fn is None:
            raise NotImplementedEmit(f"instrukcja: {tag}")
        fn(node)

    def emit_if(self, node: tuple) -> None:
        cond, then_stmt, else_stmt = node[1], node[2], node[3]
        self.emit_line(f"if ({self.emit_expr(cond)}) {{")
        self.indent()
        self.emit_stmt(then_stmt)
        self.dedent()
        if else_stmt is not None:
            self.emit_line("} else {")
            self.indent()
            self.emit_stmt(else_stmt)
            self.dedent()
        self.emit_line("}")

    def emit_return(self, node: tuple) -> None:
        if node[1] is None:
            self.emit_line("return;")
        else:
            self.emit_line(f"return {self.emit_expr(node[1])};")

    def emit_repeat(self, node: tuple) -> None:
        stmts, cond = node[1], node[2]
        self.emit_line("do {")
        self.indent()
        for stmt in stmts:
            self.emit_stmt(stmt)
        self.dedent()
        self.emit_line(f"}} while (!({self.emit_expr(cond)}));")

    def emit_case(self, node: tuple) -> None:
        expr, arms, else_stmt = node[1], node[2], node[3]
        self.emit_line(f"switch ({self.emit_expr(expr)}) {{")
        for arm in arms:
            if arm[0] != "CaseArm":
                raise ValueError(f"Oczekiwano CaseArm, jest {arm[0]!r}")
            labels, stmt = arm[1], arm[2]
            for label in labels:
                self.emit_line(f"case {self.emit_expr(label)}:")
            self.indent()
            self.emit_stmt(stmt)
            self.emit_line("break;")
            self.dedent()
        if else_stmt is not None:
            self.emit_line("default:")
            self.indent()
            self.emit_stmt(else_stmt)
            self.emit_line("break;")
            self.dedent()
        self.emit_line("}")

    def emit_expr_stmt(self, node: tuple) -> None:
        expr = node[1]
        if expr[0] != "Call":
            raise NotImplementedEmit(f"expr_stmt: {expr[0]!r}")
        self.emit_call(expr)

    def emit_call(self, node: tuple) -> None:
        name, args = node[1], node[2] or []
        args_e = ", ".join(self.emit_expr(a) for a in args)
        self.emit_line(f"{name}({args_e});")

    def emit_while(self, node: tuple) -> None:
        cond, body = node[1], node[2]
        self.emit_line(f"while ({self.emit_expr(cond)}) {{")
        self.indent()
        self.emit_stmt(body)
        self.dedent()
        self.emit_line("}")

    def emit_print(self, node: tuple) -> None:
        for expr in node[1] or []:
            self._emit_print_item(expr)

    def _scan_format(self, expr: tuple) -> str:
        """Format scanf/printf dla typu wyrażenia."""
        if expr[0] == "Var":
            c_type = self.var_types.get(expr[1], "int")
            if c_type == "double":
                return "%lf"
            if c_type == "char*":
                return "%s"
            if c_type == "char":
                return "%c"
            return "%d"
        if expr[0] == "Real":
            return "%lf"
        if expr[0] == "Char":
            return "%c"
        return "%d"

    def _emit_print_item(self, expr: tuple) -> None:
        tag = expr[0]
        if tag == "Str":
            self.emit_line(f"printf({expr[1]});")
            return
        fmt = self._scan_format(expr)
        if fmt == "%s":
            self.emit_line(f'printf("%s\\n", {self.emit_expr(expr)});')
        else:
            self.emit_line(f'printf("{fmt}\\n", {self.emit_expr(expr)});')

    def emit_input(self, node: tuple) -> None:
        target = node[1]
        if target[0] != "Var":
            raise NotImplementedEmit(f"input: {target[0]!r}")
        fmt = self._scan_format(target)
        self.emit_line(f'scanf("{fmt}", &{target[1]});')

    def emit_for(self, node: tuple) -> None:
        loop_var, start, end, direction, body = node[1], node[2], node[3], node[4], node[5]
        start_e = self.emit_expr(start)
        end_e = self.emit_expr(end)
        if direction == "TO":
            self.emit_line(
                f"for ({loop_var} = {start_e}; {loop_var} <= {end_e}; {loop_var}++) {{"
            )
        elif direction == "DOWNTO":
            self.emit_line(
                f"for ({loop_var} = {start_e}; {loop_var} >= {end_e}; {loop_var}--) {{"
            )
        else:
            raise NotImplementedEmit(f"for: {direction}")
        self.indent()
        self.emit_stmt(body)
        self.dedent()
        self.emit_line("}")

    def emit_assign(self, node: tuple) -> None:
        lhs, rhs = node[1], node[2]
        self.emit_line(f"{self.emit_lvalue(lhs)} = {self.emit_expr(rhs)};")

    def emit_lvalue(self, node: tuple) -> str:
        if node[0] == "Var":
            return node[1]
        if node[0] == "Index":
            base, index_expr = node[1], node[2]
            if base[0] != "Var":
                raise NotImplementedEmit(f"index base: {base[0]!r}")
            name = base[1]
            low, _high = self.array_bounds[name]
            return f"{name}[({self.emit_expr(index_expr)} - {low})]"
        raise NotImplementedEmit(f"lvalue: {node[0]!r}")

    def emit_expr(self, node: tuple) -> str:
        tag = node[0]
        if tag == "Int":
            return str(node[1])
        if tag == "Real":
            return str(node[1])
        if tag == "Char":
            return node[1]
        if tag == "Var":
            return node[1]
        if tag == "Bool":
            return "1" if node[1] == "true" else "0"
        if tag == "Str":
            return node[1]
        if tag == "BinOp":
            return self.emit_binop(node)
        if tag == "UnaryNot":
            return f"(!{self.emit_expr(node[1])})"
        if tag == "Call":
            name, args = node[1], node[2] or []
            args_e = ", ".join(self.emit_expr(a) for a in args)
            return f"{name}({args_e})"
        if tag == "Index":
            return self.emit_lvalue(node)
        if tag == "Cast":
            expr, type_name = node[1], node[2]
            c_type = self.type_to_c(type_name)
            return f"(({c_type}){self.emit_expr(expr)})"
        raise NotImplementedEmit(f"wyrazenie: {tag}")

    def emit_binop(self, node: tuple) -> str:
        op, left, right = node[1], node[2], node[3]
        left_e = self.emit_expr(left)
        right_e = self.emit_expr(right)
        c_ops = {
            "PLUS": "+",
            "MINUS": "-",
            "MUL": "*",
            "DIV": "/",
            "MOD": "%",
            "EQ": "==",
            "NEQ": "!=",
            "LT": "<",
            "LE": "<=",
            "GT": ">",
            "GE": ">=",
            "AND": "&&",
            "OR": "||",
        }
        if op in c_ops:
            return f"({left_e} {c_ops[op]} {right_e})"
        raise NotImplementedEmit(f"operator: {op}")


def emit_c(ast: tuple) -> str:
    ctx = EmitContext()
    ctx.emit_program(ast)
    return ctx.render()
