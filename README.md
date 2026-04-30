EmojiPascal – Transpiler języka opartego na Pascalu na język C

## Dane autorów
* **Imię i Nazwisko:** Alicja Kwiatkowska 
  **E-mail:** kwiatkowskaa@student.agh.edu.pl
* **Imię i Nazwisko:** Dawid Kałucki
  **E-mail:** dkalucki@student.agh.edu.pl

---

## Założenia programu

### Ogólne cele programu
Celem projektu jest stworzenie narzędzia do translacji autorskiego języka opartego na składni Pascala, o nazwie **EmojiPascal**, w którym standardowe słowa kluczowe zostały zastąpione odpowiednimi symbolami Emoji. Projekt skupia się na praktycznej implementacji pełnego procesu konwersji: od odczytania znaków Emoji, przez analizę struktury programu, aż po wygenerowanie gotowego kodu w języku C.

### Rodzaj translatora
Program jest **konwerterem (transpilerem)**, który dokonuje translacji kodu źródłowego wysokiego poziomu na inny kod źródłowy wysokiego poziomu.

### Planowany wynik działania programu
Kompilator (transpiler) języka **EmojiPascal do kodu źródłowego języka C**. Kod wynikowy będzie gotowy do bezpośredniej kompilacji przy użyciu kompilatora `gcc`.

### Planowany język implementacji
* **Python 3.10+** <!--?? -->

### Sposób realizacji skanera/parsera
Do realizacji analizy leksykalnej i składniowej zostanie wykorzystana biblioteka:

* **PLY (Python Lex-Yacc)** – narzędzie implementujące mechanizmy znane z Lex i Yacc w języku Python, umożliwiające definiowanie tokenów oraz gramatyki w sposób formalny (LALR).

Biblioteka pozwala na:
- implementację analizatora leksykalnego (lexer),
- implementację analizatora składniowego (parser),
- obsługę znaków Unicode (w tym emoji).

---

## Opis tokenów
Pełna specyfikacja mapowania symboli Emoji na tokeny znajduje się w osobnym pliku dokumentacji:  
👉 [Dokumentacja Tokenów](./docs/tokeny.md)

### Przykładowe mapowania:
| Słowo kluczowe | Emoji | Opis |
|:---|:---:|:---|
| `PROGRAM` | `🏁` | Początek programu |
| `IF` | `❓` | Instrukcja warunkowa |
| `ASSIGN` | `⬅️` | Operacja przypisania |
| `LPAREN` | `🤜` | Lewy nawias |

---

## Przykładowy program

Poniżej przedstawiono przykładowy program w języku **EmojiPascal** zapisany w pliku o rozszerzeniu `.ep`.

📄 **Plik:** `najwiekszy_wspolny_dzielnik.ep`

Program przyjmuje od użytkownika dwie liczby całkowite, znajduje ich największy wspólny dzielnik, a następnie wypisuje wynik:

```ep
🏁 NajwiekszyWspolnyDzielnik 🔹

📦
    a 📍 🔢 🔹
    b 📍 🔢 🔹
    temp 📍 🔢 🔹

🚦
    🖨️ 🤜 "Podaj pierwsza liczbe: " 🤛 🔹
    📥 🤜 a 🤛 🔹
    🖨️ 🤜 "Podaj druga liczbe: " 🤛 🔹
    📥 🤜 b 🤛 🔹

    🔁 b ❌ 0️⃣ ▶️
        🚦
            temp ⬅️ b 🔹
            b ⬅️ a ✂️ b 🔹
            a ⬅️ temp 🔹
        🛑 🔹

    🖨️ 🤜 "Najwiekszy wspolny dzielnik to: " 🤛 🔹
    🖨️ 🤜 a 🤛 🔹
🛑 🔚
```

---

## Gramatyka formatu
Gramatyka zostanie zaimplementowana w notacji generatora **PLY**. Ponizej znajduje sie docelowa wersja EmojiPascal z podzialem tematycznym (parser, deklaracje, instrukcje, wyrazenia), wzorowana na klasycznym Pascalu.

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

## Struktura projektu
* `/src` – kod źródłowy transpilera (Lexer, Parser, Generator kodu).
* `/docs` – dokumentacja techniczna, spis tokenów oraz gramatyka projektu.
* `/examples` – przykładowe programy w języku EmojiPascal (pliki `.ep`).  <!--albo inne rozszerzenie -->
* `/output` – wygenerowane pliki źródłowe w języku C.