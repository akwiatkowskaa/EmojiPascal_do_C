"""
Parser PLY dla EmojiPascal — zgodny z README + examples/test.ep.

Lista instrukcji: stmt (SEMICOLON stmt)* — średnik jak separator w Pascalu,
więc `if ... then ... else` nie wymaga 🔹 miedzy gałęziami.
"""

from __future__ import annotations

import ply.yacc as yacc

from lexer import lexer, tokens  # noqa: F401

precedence = (
    ("left", "OR"),
    ("left", "AND"),
    ("right", "NOT"),
    ("nonassoc", "EQ", "NEQ", "LT", "LE", "GT", "GE"),
    ("left", "PLUS", "MINUS"),
    ("left", "MUL", "DIV", "MOD"),
    ("right", "UMINUS", "UPLUS"),
    # RPAREN: zamknięcie '(' po wywołaniu / indeksie — najpierw redukuj listę argumentów.
    ("left", "RPAREN"),
    ("left", "ARG_EXPR_LIST"),
    # Niżej niż POSTFIX_CALL — przy 🔹 redukujemy wywołanie (nie „shift” średnika).
    ("left", "SEMICOLON"),
    ("left", "POSTFIX_CALL"),
    # arr(i) ⬅️ ... — po ) nie kończymy na wywołaniu, tylko przypisujemy.
    ("left", "ASSIGN"),
)


def p_program(p):
    "program : PROGRAM IDENTIFIER SEMICOLON block DOT"
    p[0] = ("Program", p[2], p[4])


def p_block(p):
    "block : const_section_opt var_section_opt subprogram_decls_opt compound_stmt"
    p[0] = ("Block", p[1], p[2], p[3], p[4])


# --- const ---


def p_const_section_opt_none(p):
    "const_section_opt : empty"
    p[0] = []


def p_const_section_opt_some(p):
    "const_section_opt : CONST const_decl_list"
    p[0] = p[2]


def p_const_decl_list_one(p):
    "const_decl_list : const_decl"
    p[0] = [p[1]]


def p_const_decl_list_many(p):
    "const_decl_list : const_decl_list const_decl"
    p[0] = p[1] + [p[2]]


def p_const_decl(p):
    "const_decl : IDENTIFIER EQ literal_const SEMICOLON"
    p[0] = ("ConstDecl", p[1], p[3])


def p_literal_const_int(p):
    "literal_const : LITERAL_INT"
    p[0] = ("Int", p[1])


def p_literal_const_real(p):
    "literal_const : LITERAL_REAL"
    p[0] = ("Real", p[1])


def p_literal_const_str(p):
    "literal_const : LITERAL_STR"
    p[0] = ("Str", p[1])


def p_literal_const_bool(p):
    "literal_const : LITERAL_BOOL"
    p[0] = ("Bool", p[1])


def p_literal_const_char(p):
    "literal_const : LITERAL_CHAR"
    p[0] = ("Char", p[1])


# --- var ---


def p_var_section_opt_none(p):
    "var_section_opt : empty"
    p[0] = []


def p_var_section_opt_some(p):
    "var_section_opt : VAR var_decl_list"
    p[0] = p[2]


def p_var_decl_list_one(p):
    "var_decl_list : var_decl"
    p[0] = [p[1]]


def p_var_decl_list_many(p):
    "var_decl_list : var_decl_list var_decl"
    p[0] = p[1] + [p[2]]


def p_var_decl(p):
    "var_decl : id_list COLON type_name SEMICOLON"
    p[0] = ("VarDecl", p[1], p[3])


def p_id_list_one(p):
    "id_list : IDENTIFIER"
    p[0] = [p[1]]


def p_id_list_many(p):
    "id_list : id_list COMMA IDENTIFIER"
    p[0] = p[1] + [p[3]]


def p_type_name_simple(p):
    """type_name : TYPE_INT
    | TYPE_REAL
    | TYPE_STRING
    | TYPE_BOOL
    | TYPE_CHAR"""
    p[0] = ("TypeSimple", p.slice[1].type)


def p_type_name_array(p):
    "type_name : ARRAY LPAREN expr RANGE expr RPAREN OF type_base"
    p[0] = ("TypeArray", p[3], p[5], p[8])


def p_type_base(p):
    """type_base : TYPE_INT
    | TYPE_REAL
    | TYPE_STRING
    | TYPE_BOOL
    | TYPE_CHAR"""
    p[0] = p.slice[1].type


# --- podprogramy ---


def p_subprogram_decls_opt_none(p):
    "subprogram_decls_opt : empty"
    p[0] = []


def p_subprogram_decls_opt_some(p):
    "subprogram_decls_opt : subprogram_list"
    p[0] = p[1]


def p_subprogram_list_one(p):
    "subprogram_list : subprogram_decl"
    p[0] = [p[1]]


def p_subprogram_list_many(p):
    "subprogram_list : subprogram_list subprogram_decl"
    p[0] = p[1] + [p[2]]


def p_subprogram_decl_proc(p):
    "subprogram_decl : proc_decl"
    p[0] = p[1]


def p_subprogram_decl_func(p):
    "subprogram_decl : func_decl"
    p[0] = p[1]


def p_proc_decl(p):
    "proc_decl : PROCEDURE IDENTIFIER formal_params_opt SEMICOLON inner_block SEMICOLON"
    p[0] = ("Procedure", p[2], p[3], p[5])


def p_func_decl(p):
    "func_decl : FUNCTION IDENTIFIER formal_params_opt COLON type_name SEMICOLON inner_block SEMICOLON"
    p[0] = ("Function", p[2], p[3], p[5], p[7])


def p_inner_block(p):
    "inner_block : var_section_opt compound_stmt"
    p[0] = ("InnerBlock", p[1], p[2])


def p_formal_params_opt_none(p):
    "formal_params_opt : empty"
    p[0] = []


def p_formal_params_opt_some(p):
    "formal_params_opt : LPAREN formal_param_list RPAREN"
    p[0] = p[2]


def p_formal_param_list_one(p):
    "formal_param_list : formal_param_group"
    p[0] = [p[1]]


def p_formal_param_list_many(p):
    "formal_param_list : formal_param_list SEMICOLON formal_param_group"
    p[0] = p[1] + [p[3]]


def p_formal_param_group_plain(p):
    "formal_param_group : id_list COLON type_name"
    p[0] = ("Param", False, p[1], p[3])


def p_formal_param_group_var(p):
    "formal_param_group : BYREF id_list COLON type_name"
    p[0] = ("Param", True, p[2], p[4])


# --- compound / stmt_list: średnik jako separator ---


def p_compound_stmt(p):
    "compound_stmt : BEGIN stmt_list_opt END"
    p[0] = ("Compound", p[2])


def p_stmt_list_opt_none(p):
    "stmt_list_opt : empty"
    p[0] = []


def p_stmt_list_opt_some(p):
    "stmt_list_opt : stmt_list"
    p[0] = p[1]


def p_stmt_list_one(p):
    "stmt_list : stmt SEMICOLON"
    p[0] = [p[1]]


def p_stmt_list_many(p):
    "stmt_list : stmt_list stmt SEMICOLON"
    p[0] = p[1] + [p[2]]


def p_stmt_assign(p):
    "stmt : assign_stmt"
    p[0] = p[1]


def p_stmt_print(p):
    "stmt : print_stmt"
    p[0] = p[1]


def p_stmt_input(p):
    "stmt : input_stmt"
    p[0] = p[1]


def p_stmt_for(p):
    "stmt : for_stmt"
    p[0] = p[1]


def p_stmt_if(p):
    "stmt : if_stmt"
    p[0] = p[1]


def p_stmt_while(p):
    "stmt : while_stmt"
    p[0] = p[1]


def p_stmt_repeat(p):
    "stmt : repeat_stmt"
    p[0] = p[1]


def p_stmt_case(p):
    "stmt : case_stmt"
    p[0] = p[1]


def p_stmt_return(p):
    "stmt : return_stmt"
    p[0] = p[1]


def p_stmt_expr(p):
    "stmt : expr"
    p[0] = ("ExprStmt", p[1])


def p_stmt_compound(p):
    "stmt : compound_stmt"
    p[0] = p[1]


def p_assign_stmt_simple(p):
    "assign_stmt : var_ref ASSIGN expr"
    p[0] = ("Assign", p[1], p[3])


def p_assign_stmt_indexed(p):
    "assign_stmt : IDENTIFIER LPAREN expr_list_opt RPAREN ASSIGN expr"
    if not p[3]:
        raise SyntaxError("Przypisanie do tablicy wymaga co najmniej jednego indeksu")
    lhs: tuple = ("Var", p[1])
    for ix in p[3]:
        lhs = ("Index", lhs, ix)
    p[0] = ("Assign", lhs, p[6])


def p_print_stmt(p):
    "print_stmt : PRINT LPAREN expr_list_opt RPAREN"
    p[0] = ("Print", p[3])


def p_input_stmt(p):
    "input_stmt : INPUT LPAREN var_ref RPAREN"
    p[0] = ("Input", p[3])


def p_for_stmt_to(p):
    "for_stmt : FOR IDENTIFIER ASSIGN expr TO expr DO stmt"
    p[0] = ("For", p[2], p[4], p[6], "TO", p[8])


def p_for_stmt_downto(p):
    "for_stmt : FOR IDENTIFIER ASSIGN expr DOWNTO expr DO stmt"
    p[0] = ("For", p[2], p[4], p[6], "DOWNTO", p[8])


def p_if_stmt(p):
    "if_stmt : IF expr THEN stmt else_opt"
    p[0] = ("If", p[2], p[4], p[5])


def p_else_opt_some(p):
    "else_opt : ELSE stmt"
    p[0] = p[2]


def p_else_opt_none(p):
    "else_opt : empty"
    p[0] = None


def p_while_stmt(p):
    "while_stmt : WHILE expr DO stmt"
    p[0] = ("While", p[2], p[4])


def p_repeat_stmt(p):
    "repeat_stmt : REPEAT stmt_list UNTIL expr"
    p[0] = ("Repeat", p[2], p[4])


def p_case_stmt(p):
    "case_stmt : CASE expr OF case_arm_list case_else_opt END"
    p[0] = ("Case", p[2], p[4], p[5])


def p_case_arm_list_one(p):
    "case_arm_list : case_arm"
    p[0] = [p[1]]


def p_case_arm_list_many(p):
    "case_arm_list : case_arm_list case_arm"
    p[0] = p[1] + [p[2]]


def p_case_arm(p):
    "case_arm : literal_const_list THEN stmt SEMICOLON"
    p[0] = ("CaseArm", p[1], p[3])


def p_literal_const_list_one(p):
    "literal_const_list : literal_const"
    p[0] = [p[1]]


def p_literal_const_list_many(p):
    "literal_const_list : literal_const_list COMMA literal_const"
    p[0] = p[1] + [p[3]]


def p_case_else_some(p):
    "case_else_opt : ELSE stmt SEMICOLON"
    p[0] = p[2]


def p_case_else_none(p):
    "case_else_opt : empty"
    p[0] = None


def p_return_stmt_expr(p):
    "return_stmt : RETURN expr"
    p[0] = ("Return", p[2])


def p_return_stmt_void(p):
    "return_stmt : RETURN"
    p[0] = ("Return", None)



# --- wyrazenia ---


def p_expr_bool(p):
    "expr : bool_or"
    p[0] = p[1]


def p_bool_or_bin(p):
    "bool_or : bool_or OR bool_and"
    p[0] = ("BinOp", "OR", p[1], p[3])


def p_bool_or_one(p):
    "bool_or : bool_and"
    p[0] = p[1]


def p_bool_and_bin(p):
    "bool_and : bool_and AND bool_not"
    p[0] = ("BinOp", "AND", p[1], p[3])


def p_bool_and_one(p):
    "bool_and : bool_not"
    p[0] = p[1]


def p_bool_not_not(p):
    "bool_not : NOT bool_not"
    p[0] = ("UnaryNot", p[2])


def p_bool_not_rel(p):
    "bool_not : relational"
    p[0] = p[1]


def p_relational_cmp(p):
    "relational : math_expr rel_op math_expr"
    p[0] = ("BinOp", p[2], p[1], p[3])


def p_rel_op_tokens(p):
    """rel_op : EQ
    | NEQ
    | LT
    | LE
    | GT
    | GE"""
    p[0] = p.slice[1].type


def p_relational_math(p):
    "relational : math_expr"
    p[0] = p[1]


def p_math_expr_bin_plus(p):
    "math_expr : math_expr PLUS math_term"
    p[0] = ("BinOp", "PLUS", p[1], p[3])


def p_math_expr_bin_minus(p):
    "math_expr : math_expr MINUS math_term"
    p[0] = ("BinOp", "MINUS", p[1], p[3])


def p_math_expr_term(p):
    "math_expr : math_term"
    p[0] = p[1]


def p_math_term_mul(p):
    "math_term : math_term MUL math_factor"
    p[0] = ("BinOp", "MUL", p[1], p[3])


def p_math_term_div(p):
    "math_term : math_term DIV math_factor"
    p[0] = ("BinOp", "DIV", p[1], p[3])


def p_math_term_mod(p):
    "math_term : math_term MOD math_factor"
    p[0] = ("BinOp", "MOD", p[1], p[3])


def p_math_term_factor(p):
    "math_term : math_factor"
    p[0] = p[1]


def p_math_factor_uplus(p):
    "math_factor : PLUS math_factor %prec UPLUS"
    p[0] = ("UnaryPlus", p[2])


def p_math_factor_uminus(p):
    "math_factor : MINUS math_factor %prec UMINUS"
    p[0] = ("UnaryMinus", p[2])


def p_math_factor_primary(p):
    "math_factor : primary"
    p[0] = p[1]


def p_primary_num_int(p):
    "primary : LITERAL_INT"
    p[0] = ("Int", p[1])


def p_primary_num_real(p):
    "primary : LITERAL_REAL"
    p[0] = ("Real", p[1])


def p_primary_str(p):
    'primary : LITERAL_STR'
    p[0] = ("Str", p[1])


def p_primary_bool(p):
    "primary : LITERAL_BOOL"
    p[0] = ("Bool", p[1])


def p_primary_char(p):
    "primary : LITERAL_CHAR"
    p[0] = ("Char", p[1])


def p_primary_call(p):
    "primary : IDENTIFIER LPAREN expr_list_opt RPAREN %prec POSTFIX_CALL"
    p[0] = ("Call", p[1], p[3])


def p_primary_var(p):
    "primary : var_ref"
    p[0] = p[1]


def p_primary_paren(p):
    "primary : LPAREN expr RPAREN"
    p[0] = p[2]


def p_primary_cast(p):
    "primary : CAST LPAREN expr RPAREN COLON type_name"
    p[0] = ("Cast", p[3], p[6])


def p_var_ref_id(p):
    "var_ref : IDENTIFIER"
    p[0] = ("Var", p[1])


def p_var_ref_field(p):
    "var_ref : var_ref FIELD_ACCESS IDENTIFIER"
    p[0] = ("Field", p[1], p[3])


def p_expr_list_opt_empty(p):
    "expr_list_opt : empty"
    p[0] = []


def p_expr_list_opt_some(p):
    "expr_list_opt : expr_list"
    p[0] = p[1]


def p_expr_list_one(p):
    "expr_list : expr %prec ARG_EXPR_LIST"
    p[0] = [p[1]]


def p_expr_list_many(p):
    "expr_list : expr_list COMMA expr"
    p[0] = p[1] + [p[3]]


def p_empty(p):
    "empty :"
    pass


def p_error(p):
    if p is None:
        raise SyntaxError("Nieoczekiwany koniec pliku (brak tokenow / niepelna skladnia)")
    raise SyntaxError(
        f"Blad skladni przy tokenie {p.type} {p.value!r} (linia {p.lineno})"
    )


parser = yacc.yacc(write_tables=False, debug=False)


def parse_source(text: str):
    lexer.input(text)
    return parser.parse(text, lexer=lexer)
