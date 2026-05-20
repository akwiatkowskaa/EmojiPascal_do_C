"""Emiter kodu C z drzewa AST EmojiPascal (tuple z parser.py)."""

from __future__ import annotations


class NotImplementedEmit(NotImplementedError):
    """Brak emisji dla węzła AST — kolejna faza planu."""


class EmitContext:
    def __init__(self) -> None:
        self.lines: list[str] = []
        self.indent_level = 0

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
        self.emit_line("int main(void) {")
        self.indent()
        self.emit_block(block)
        self.emit_line("return 0;")
        self.dedent()
        self.emit_line("}")

    def emit_block(self, node: tuple) -> None:
        if node[0] != "Block":
            raise ValueError(f"Oczekiwano Block, jest {node[0]!r}")
        _const_section, var_section, _subprograms, compound = (
            node[1],
            node[2],
            node[3],
            node[4],
        )
        for var_decl in var_section:
            self.emit_var_decl(var_decl)
        if var_section and compound[1]:
            self.emit_line("")
        self.emit_compound(compound)

    def emit_var_decl(self, node: tuple) -> None:
        if node[0] != "VarDecl":
            raise ValueError(f"Oczekiwano VarDecl, jest {node[0]!r}")
        id_list, type_name = node[1], node[2]
        c_type = self.type_to_c(type_name)
        names = ", ".join(id_list)
        self.emit_line(f"{c_type} {names};")

    def type_to_c(self, type_node: tuple) -> str:
        if type_node[0] != "TypeSimple":
            raise NotImplementedEmit(f"typ: {type_node[0]!r}")
        token = type_node[1]
        if token == "TYPE_INT":
            return "int"
        raise NotImplementedEmit(f"typ: {token}")

    def emit_compound(self, node: tuple) -> None:
        if node[0] != "Compound":
            raise ValueError(f"Oczekiwano Compound, jest {node[0]!r}")
        for stmt in node[1]:
            self.emit_stmt(stmt)

    def emit_stmt(self, node: tuple) -> None:
        tag = node[0]
        if tag == "Assign":
            self.emit_assign(node)
            return
        if tag == "Compound":
            self.emit_compound(node)
            return
        if tag == "Print":
            self.emit_print(node)
            return
        if tag == "Input":
            self.emit_input(node)
            return
        if tag == "For":
            self.emit_for(node)
            return
        raise NotImplementedEmit(f"instrukcja: {tag}")

    def emit_print(self, node: tuple) -> None:
        if node[0] != "Print":
            raise ValueError(f"Oczekiwano Print, jest {node[0]!r}")
        for expr in node[1] or []:
            self._emit_print_item(expr)

    def _emit_print_item(self, expr: tuple) -> None:
        tag = expr[0]
        if tag == "Str":
            # Literał w AST ma już cudzysłowy, np. "Podaj n: "
            self.emit_line(f"printf({expr[1]});")
            return
        if tag in ("Int", "Var", "BinOp"):
            self.emit_line(f'printf("%d\\n", {self.emit_expr(expr)});')
            return
        raise NotImplementedEmit(f"print arg: {tag}")

    def emit_input(self, node: tuple) -> None:
        if node[0] != "Input":
            raise ValueError(f"Oczekiwano Input, jest {node[0]!r}")
        target = node[1]
        if target[0] != "Var":
            raise NotImplementedEmit(f"input: {target[0]!r}")
        self.emit_line(f'scanf("%d", &{target[1]});')

    def emit_for(self, node: tuple) -> None:
        if node[0] != "For":
            raise ValueError(f"Oczekiwano For, jest {node[0]!r}")
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
        if node[0] != "Assign":
            raise ValueError(f"Oczekiwano Assign, jest {node[0]!r}")
        lhs, rhs = node[1], node[2]
        if lhs[0] != "Var":
            raise NotImplementedEmit(f"przypisanie lhs: {lhs[0]!r}")
        self.emit_line(f"{lhs[1]} = {self.emit_expr(rhs)};")

    def emit_expr(self, node: tuple) -> str:
        tag = node[0]
        if tag == "Int":
            return str(node[1])
        if tag == "Var":
            return node[1]
        if tag == "BinOp":
            return self.emit_binop(node)
        raise NotImplementedEmit(f"wyrazenie: {tag}")

    def emit_binop(self, node: tuple) -> str:
        op, left, right = node[1], node[2], node[3]
        left_e = self.emit_expr(left)
        right_e = self.emit_expr(right)
        if op == "PLUS":
            return f"({left_e} + {right_e})"
        if op == "MINUS":
            return f"({left_e} - {right_e})"
        raise NotImplementedEmit(f"operator: {op}")


def emit_c(ast: tuple) -> str:
    ctx = EmitContext()
    ctx.emit_program(ast)
    return ctx.render()
