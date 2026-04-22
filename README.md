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

## Gramatyka formatu
Gramatyka zostanie zaimplementowana w notacji generatora **PLY**. Poniżej przedstawiono wstępny zarys struktury języka w notacji zbliżonej do BNF:

```bnf
<program> ::= 🏁 <id> 🔹 <declarations> <functions> 🚦 <statements> 🛑 🔚

<declarations> ::= 📦 <decl_list> | ε

<decl_list> ::= <decl> 🔹 <decl_list> | <decl>

<decl> ::= <id_list> 📍 <type>

<id_list> ::= <id> | <id> 📎 <id_list>

<type> ::= 🔢 | 🧵 | ✅ | 📚 🤜 <math_expr> 🤛 <type>

<functions> ::= <func_decl> 🔹 <functions> | ε

<func_decl> ::= ⚙️ <id> 🤜 <params> 🤛 📍 <type> 🚦 <statements> 🛑

<params> ::= <param_list> | ε

<param_list> ::= <id> 📍 <type> | <id> 📍 <type> 📎 <param_list>

<statements> ::= <stmt> 🔹 <statements> | <stmt>

<stmt> ::= <assign_stmt>
         | <if_stmt>
         | <while_stmt>
         | <print_stmt>
         | <input_stmt>
         | <return_stmt>

<assign_stmt> ::= <var_ref> ⬅️ <expression>

<input_stmt> ::= 📥 🤜 <var_ref> 🤛

<return_stmt> ::= ↩️ <expression>

<if_stmt> ::= ❓ <expression> ➡️ <stmt> [ 🙅 <stmt> ]

<while_stmt> ::= 🔁 <expression> ▶️ <stmt>

<print_stmt> ::= 🖨️ 🤜 <expression> 🤛

<expression> ::= <logic_expr>

<logic_expr> ::= <rel_expr>
               | <logic_expr> 🤝 <rel_expr>
               | <logic_expr> 🔀 <rel_expr>
               | 🚫 <rel_expr>

<rel_expr> ::= <math_expr>
             | <math_expr> 🟰 <math_expr>
             | <math_expr> ❌ <math_expr>
             | <math_expr> 🔽 <math_expr>
             | <math_expr> ⏬ <math_expr>
             | <math_expr> 🔼 <math_expr>
             | <math_expr> ⏫ <math_expr>

<math_expr> ::= <term>
              | <math_expr> ➕ <term>
              | <math_expr> ➖ <term>

<term> ::= <factor>
         | <term> ✖️ <factor>
         | <term> ➗ <factor>

<factor> ::= <var_ref>
           | <literal>
           | <func_call>
           | <conversion>
           | 🤜 <expression> 🤛

<var_ref> ::= <id> | <id> 🤜 <math_expr> 🤛

<func_call> ::= <id> 🤜 <arg_list> 🤛

<arg_list> ::= <expression> | <expression> 📎 <arg_list> | ε

<conversion> ::= ✨ 🤜 <expression> 🤛 📍 <type>

<literal> ::= LITERAL_INT
            | LITERAL_STR
            | LITERAL_BOOL

<id> ::= IDENTIFIER
```

---

## Struktura projektu
* `/src` – kod źródłowy transpilera (Lexer, Parser, Generator kodu).
* `/docs` – dokumentacja techniczna, spis tokenów oraz gramatyka projektu.
* `/examples` – przykładowe programy w języku EmojiPascal (pliki `.ep`).  <!--albo inne rozszerzenie -->
* `/output` – wygenerowane pliki źródłowe w języku C.