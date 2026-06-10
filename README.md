EmojiPascal – transpiler języka opartego na Pascalu na język C

## Dane studentów
- Imię i nazwisko: Alicja Kwiatkowska
- Imię i nazwisko: Dawid Kałucki

## Dane kontaktowe
- E-mail: kwiatkowskaa@student.agh.edu.pl
- E-mail: dkalucki@student.agh.edu.pl

---

## Założenia programu

### Ogólne cele programu
Celem projektu jest stworzenie narzędzia do translacji autorskiego języka EmojiPascal, w którym słowa kluczowe i część składni zostały zapisane emoji. Program realizuje pełny proces: skanowanie tokenów, analizę składniową, analizę semantyczną oraz wygenerowanie kodu C.

### Rodzaj translatora
Projekt jest **konwerterem (kompilatorem/transpilerem)**: wejście to program w EmojiPascal (`.ep`), wyjście to program w C (`.c`).

### Planowany wynik działania programu
Wynikiem działania jest kod C możliwy do kompilacji kompilatorem `gcc`.

### Planowany język implementacji
Implementacja: **Python 3.10+**.

### Sposób realizacji skanera/parsera
Skaner i parser są wykonane z użyciem generatora **PLY (Python Lex-Yacc)**:
- skaner: `src/lexer.py`,
- parser: `src/parser.py`.

---

## Opis tokenów

Pełny opis tokenów jest w pliku [`docs/tokeny.md`](./docs/tokeny.md).

Przykładowe tokeny:

| Nazwa tokenu | Emoji / zapis | Opis |
|:---|:---:|:---|
| `PROGRAM` | `🏁` | początek programu |
| `VAR` | `📦` | sekcja zmiennych |
| `BEGIN` | `🚦` | początek bloku |
| `END` | `🛑` | koniec bloku |
| `ASSIGN` | `⬅️` | przypisanie |
| `SEMICOLON` | `🔹` | separator instrukcji |
| `TYPE_INT` | `🔢` | typ całkowity |
| `LITERAL_BOOL` | `👍` / `👎` | stałe logiczne |

---

## Gramatyka formatu
Poniżej zestawiono **docelową** specyfikację składni w notacji zbliżonej do **BNF**, wzorowaną na klasycznym Pascalu. **Implementacja** reguł w generatorze **PLY** znajduje się w pliku [`src/parser.py`](./src/parser.py); w razie rozbieżności szczegółowych (np. zapis listy instrukcji, wywołania) **źródłem prawdy** jest kod parsera oraz programy przykładowe w katalogu `examples/`.

```bnf
// ==========================================
// PARSER - STRUKTURA PROGRAMU
// ==========================================
<program> ::= 🏁 <id> 🔹 <block> 🔚

<block> ::= <const_section_opt> <var_section_opt> <subprogram_decls_opt> 🚦 <stmt_list_opt> 🛑

// ==========================================
// DEKLARACJE
// ==========================================
<const_section_opt> ::= <const_section> | ε
<const_section> ::= 📌 <const_decl_list>
<const_decl_list> ::= <const_decl> 🔹 <const_decl_list> | <const_decl> 🔹
<const_decl> ::= <id> 🟰 <const_value>

<var_section_opt> ::= <var_section> | ε
<var_section> ::= 📦 <var_decl_list>
<var_decl_list> ::= <var_decl> 🔹 <var_decl_list> | <var_decl> 🔹
<var_decl> ::= <id_list> 📍 <type>

<id_list> ::= <id> | <id> 📎 <id_list>


// --- typy ---
<type> ::= 🔢 | 🌊 | 🧵 | ✅ | 🔡
         | 📚 🤜 <const_int> ↔️ <const_int> 🤛 🧾 <type>
         | 🧱 🚦 <field_decl_list> 🛑

<field_decl_list> ::= <field_decl> 🔹 <field_decl_list> | <field_decl> 🔹
<field_decl> ::= <id_list> 📍 <type>


// ==========================================
// PODPROGRAMY
// ==========================================
<subprogram_decls_opt> ::= <subprogram_decls> | ε
<subprogram_decls> ::= <subprogram_decl> 🔹 <subprogram_decls> | <subprogram_decl> 🔹
<subprogram_decl> ::= <function_decl> | <procedure_decl>

<function_decl> ::= ⚙️ <id> <formal_params_opt> 📍 <type> 🔹 <block>
<procedure_decl> ::= 🔧 <id> <formal_params_opt> 🔹 <block>

<formal_params_opt> ::= <formal_params> | ε
<formal_params> ::= 🤜 <formal_param_list> 🤛
<formal_param_list> ::= <formal_param_group>
                      | <formal_param_group> 🔹 <formal_param_list>

<formal_param_group> ::= <byref_opt> <id_list> 📍 <type>
<byref_opt> ::= 📤 | ε

// ==========================================
// INSTRUKCJE
// ==========================================
<stmt_list_opt> ::= <stmt_list> | ε
<stmt_list> ::= <stmt> | <stmt> 🔹 <stmt_list>

<stmt> ::= <assign_stmt>
         | <proc_call_stmt>
         | <if_stmt>
         | <while_stmt>
         | <repeat_stmt>
         | <for_stmt>
         | <case_stmt>
         | <compound_stmt>
         | <print_stmt>
         | <input_stmt>
         | <return_stmt_opt>


<compound_stmt> ::= 🚦 <stmt_list_opt> 🛑

<assign_stmt> ::= <var_ref> ⬅️ <expr>

<proc_call_stmt> ::= <id>
                   | <id> 🤜 <expr_list_opt> 🤛

<expr_list_opt> ::= <expr_list> | ε
<expr_list> ::= <expr> | <expr> 📎 <expr_list>

<input_stmt> ::= 📥 🤜 <var_ref> 🤛
<print_stmt> ::= 🖨️ 🤜 <expr_list_opt> 🤛
<return_stmt_opt> ::= ↩️ <expr> | ↩️


// ==========================================
// STEROWANIE
// ==========================================
<if_stmt> ::= ❓ <bool_expr> ➡️ <stmt> <else_opt>
<else_opt> ::= 🙅 <stmt> | ε

<while_stmt> ::= 🔁 <bool_expr> ▶️ <stmt>

<repeat_stmt> ::= 🔁🔂 <stmt_list> 🔂▶️ <bool_expr>

<for_stmt> ::= 🔂 <id> ⬅️ <math_expr> ⬆️ <math_expr> ▶️ <stmt>
             | 🔂 <id> ⬅️ <math_expr> ⬇️ <math_expr> ▶️ <stmt>

<case_stmt> ::= 🧭 <expr> 🧾 <case_arm_list> <else_opt_case> 🛑
<case_arm_list> ::= <case_arm> | <case_arm> <case_arm_list>
<case_arm> ::= <const_list> ➡️ <stmt> 🔹
<const_list> ::= <const_value> | <const_value> 📎 <const_list>
<else_opt_case> ::= 🙅 <stmt> 🔹 | ε


// ==========================================
// WYRAŻENIA LOGICZNE
// ==========================================
<bool_expr> ::= <bool_expr> 🔀 <bool_term>
              | <bool_term>

<bool_term> ::= <bool_term> 🤝 <bool_factor>
              | <bool_factor>

<bool_factor> ::= 🚫 <bool_factor>
                | <bool_primary>

<bool_primary> ::= <rel_expr>
                 | <var_ref>
                 | <func_call>
                 | LITERAL_BOOL
                 | 🤜 <bool_expr> 🤛


// ==========================================
// RELACJE
// ==========================================
<rel_expr> ::= <math_expr> <rel_op> <math_expr>
<rel_op> ::= 🟰 | ❌ | 🔽 | ⏬ | 🔼 | ⏫


// ==========================================
// WYRAŻENIA MATEMATYCZNE
// ==========================================
<math_expr> ::= <math_expr> ➕ <math_term>
              | <math_expr> ➖ <math_term>
              | <math_term>

<math_term> ::= <math_term> ✖️ <math_factor>
              | <math_term> ➗ <math_factor>
              | <math_term> ✂️ <math_factor>
              | <math_factor>

<math_factor> ::= ➕ <math_factor>
                | ➖ <math_factor>
                | <math_primary>

<math_primary> ::= LITERAL_INT
                 | LITERAL_REAL
                 | <var_ref>
                 | <func_call>
                 | <conversion>
                 | 🤜 <math_expr> 🤛


// ==========================================
// POZOSTAŁE
// ==========================================
<func_call> ::= <id> 🤜 <expr_list_opt> 🤛

<var_ref> ::= <id>
            | <var_ref> 🤜 <math_expr> 🤛
            | <var_ref> 💠 <id>

<conversion> ::= ✨ 🤜 <expr> 🤛 📍 <type>

<expr> ::= <bool_expr>
         | <math_expr>
         | LITERAL_STR
         | LITERAL_CHAR

<literal> ::= LITERAL_INT | LITERAL_REAL | LITERAL_STR | LITERAL_BOOL | LITERAL_CHAR
<const_value> ::= <literal>
<const_int> ::= LITERAL_INT

<id> ::= IDENTIFIER
```

---
### Tekst gramatyki w notacji generatora parsera (PLY / Yacc-style)

Pełna gramatyka parsera jest zapisana w `src/parser.py` jako reguły `p_*`, np.:

```python
def p_program(p):
    "program : PROGRAM IDENTIFIER SEMICOLON block DOT"

def p_compound_stmt(p):
    "compound_stmt : BEGIN stmt_list_opt END"

def p_for_stmt_to(p):
    "for_stmt : FOR IDENTIFIER ASSIGN expr TO expr DO stmt"
```

---

## Stan rozszerzeń transpilera

Rozszerzenia spoza podstawowego zakresu wdrazamy stopniowo (szczegoly: [`docs/tokeny.md`](./docs/tokeny.md), sekcja 7).

| Konstrukcja | Status |
|:---|:---:|
| `real` (`🌊`, `double` w C) | tak |
| `char` (`🔡`, `char` w C) | tak |
| rzutowanie `CAST` (`✨`) | tak |
| parametry `BYREF` (`📤`) | nie |
| typ `record` (`🧱`) | nie |
| dostep do pol rekordu (`💠`) | nie |

---

## Informacje o stosowanych generatorach skanerów/parserów, pakietach zewnętrznych

- Generator skanera/parsera: **PLY (Python Lex-Yacc)**
- Pakiety zewnętrzne: `requirements.txt`
- Instalacja pakietów: `pip install -r requirements.txt`
- Moduły projektu:
  - `src/lexer.py` – skaner,
  - `src/parser.py` – parser,
  - `src/semantic.py` – analiza semantyczna,
  - `src/codegen_c.py` – emiter kodu C,
  - `src/emoji_to_pascal.py` – konwersja tekstowa emoji -> Pascal.

---

## Krótka instrukcja obsługi

Dostępne tryby:

- `python3 src/main.py <plik.ep>` – tokenizacja (lista tokenów na stdout),
- `python3 src/main.py --parse <plik.ep>` – AST (druk drzewa na stdout),
- `python3 src/main.py --emit-c <plik.ep> [wyjscie.c]` – generacja pliku C.

Domyślne lokalizacje wyników:

- C: `output/c/<nazwa>.c`
- Pascal (konwersja tekstowa): `output/pascal/<nazwa>.pas`

---

## Przykład użycia

Przykład dla programu `examples/suma_do_n.ep`.

### 1) Fragment wejścia EmojiPascal (`.ep`)

```ep
🏁 SumaDoN 🔹
📦
    n 📍 🔢 🔹
    i 📍 🔢 🔹
    suma 📍 🔢 🔹
🚦
    suma ⬅️ 0️⃣ 🔹
    🔂 i ⬅️ 1️⃣ ⬆️ n ▶️
        suma ⬅️ suma ➕ i 🔹
    🖨️ 🤜 suma 🤛 🔹
🛑 🔚
```

### 2) Jak wygląda wynik konwersji emoji -> pascal (`output/pascal/suma_do_n.pas`)

```pascal
program SumaDoN ;
var
    n : integer ;
    i : integer ;
    suma : integer ;
begin
    suma := 0 ;
    for i := 1 to n do
        suma := suma + i ;
    writeln ( suma ) ;
end .
```

### 3) Jak wygląda wynik transpilacji do C (`output/c/suma_do_n.c`)

```c
#include <stdio.h>

/* Program: SumaDoN */
int main(void) {
    int n;
    int i;
    int suma;
    printf("Podaj n: ");
    scanf("%d", &n);
    suma = 0;
    for (i = 1; i <= n; i++) {
        suma = (suma + i);
    }
    printf("Suma od 1 do n: ");
    printf("%d\\n", suma);
    return 0;
}
```

### 4) Jak wygląda wynik uruchomienia (dla `n=5`)

```text
Podaj n: 5
Suma od 1 do n:
15
```

---


### Struktura repozytorium

- `src/` – implementacja narzędzia,
- `docs/` – dokumentacja,
- `examples/` – programy wejściowe `.ep`,
- `output/c/` – wygenerowane pliki C,
- `output/pascal/` – pliki Pascal z konwersji tekstowej,
- `tests/` – testy.
