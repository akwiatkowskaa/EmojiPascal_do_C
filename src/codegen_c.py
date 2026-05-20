"""Emiter kodu C z drzewa AST EmojiPascal (tuple z parser.py)."""

from __future__ import annotations


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
        # const_section, var_section, subprograms — fazy B/F
        compound = node[4]
        self.emit_compound(compound)

    def emit_compound(self, node: tuple) -> None:
        if node[0] != "Compound":
            raise ValueError(f"Oczekiwano Compound, jest {node[0]!r}")
        # stmt_list — emisja instrukcji w fazach B–C
        _stmts = node[1]


def emit_c(ast: tuple) -> str:
    ctx = EmitContext()
    ctx.emit_program(ast)
    return ctx.render()
