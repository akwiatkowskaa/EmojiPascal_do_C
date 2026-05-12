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
Program jest **transpilerem** — dokonuje translacji kodu źródłowego w języku **EmojiPascal** na **kod źródłowy w języku C** (język implementacji narzędzia to Python, co opisano poniżej).

### Planowany wynik działania programu
Docelowym wynikiem prac jest **transpiler** języka EmojiPascal do **kodu źródłowego w języku C**, gotowego do kompilacji przy użyciu kompilatora `gcc`.

**Stan realizacji (bieżący etap):** zaimplementowano **analizę leksykalną** oraz **analizę składniową** z budową **drzewa składniowego (AST)**. **Generator kodu C** z AST pozostaje do wykonania. Dostępny jest ponadto **skrypt pomocniczy** `emoji_to_pascal.py`, który zamienia symbole emoji na odpowiedniki leksykalne w konwencji Pascala i zapisuje plik `.pas` — jest to **podstawienie tekstowe**, a nie pełna transpilacja semantyczna.

### Język implementacji i środowisko
* **Python:** wersja **3.10 lub nowsza** (zalecana aktualna stabilna wersja interpretera).
* **Biblioteka PLY** (Python Lex–Yacc) — generator analizatorów leksykalnych i składniowych w oparciu o tablice **LALR**.

Instalacja zależności Pythona dla narzędzi w `src/`:

```bash
pip install -r requirements.txt
```

W pliku [`requirements.txt`](./requirements.txt) wymienione są pakiety zewnętrzne projektu (na dziś wyłącznie **PLY**). Przy dalszej pracy (np. testy automatyczne, dodatkowe biblioteki) dopisuje się tu kolejne wiersze — współautor, prowadzący lub CI mogą wtedy zainstalować **tę samą** listę jednym poleceniem. Minimalnie wystarczy też `pip install ply`, lecz **zalecane** jest korzystanie z `requirements.txt`.

### Sposób realizacji skanera i parsera
W projekcie wykorzystywana jest biblioteka **PLY (Python Lex-Yacc)** — narzędzie implementujące mechanizmy analogiczne do Lex i Yacc w języku Python, umożliwiające formalne zdefiniowanie tokenów oraz reguł gramatyki.

PLY umożliwia w szczególności:
- implementację analizatora leksykalnego (lexer),
- implementację analizatora składniowego (parser),
- obsługę znaków Unicode (w tym emoji).

---

## Uruchomienie narzędzi

Polecenia wywołuj z **katalogu głównego repozytorium** (tam, gdzie leżą m.in. `src/` i `examples/`). Ścieżkę do pliku `.ep` podaj względem tego katalogu (np. `examples/test.ep`).

Interpreter Pythona **sam dodaje** do ścieżki importów folder zawierający uruchamiany skrypt — w przypadku `python3 src/main.py` jest to katalog `src/`, więc importy `lexer` i `parser` działają **bez** ustawiania `PYTHONPATH`.

### Analiza leksykalna (lista tokenów)
Wynik trafia na **standardowe wyjście** (`stdout`). **Nie** jest tworzony żaden plik wyjściowy.

```bash
python3 src/main.py ścieżka/do/programu.ep
```

### Analiza składniowa (AST, tryb diagnostyczny)
Po poprawnym sparsowaniu program wypisuje **drzewo składniowe** w postaci czytelnej dla człowieka. Wynik trafia na **stdout**; program **nie** zapisuje AST do pliku automatycznie.

```bash
python3 src/main.py --parse ścieżka/do/programu.ep
```

Przykładowe programy: katalog [`examples/`](./examples/) (m.in. `test.ep`, `suma_do_n.ep`).

### Eksport do pliku `.pas` (zamiana emoji na słowa kluczowe Pascala)
Skrypt wykonuje **mapowanie symboli** zgodnie z definicjami w `src/emoji_language.py`. Nie korzysta z AST.

```bash
python3 src/emoji_to_pascal.py ścieżka/do/programu.ep
```

* **Domyślna lokalizacja zapisu:** `output/pascal/<nazwa_pliku_bez_rozszerzenia>.pas` (podkatalog jest tworzony w razie potrzeby).
* **Jawna ścieżka wyjściowa:** `python3 src/emoji_to_pascal.py wejście.ep ścieżka/wyjście.pas`


---

## Opis tokenów
Pełna specyfikacja mapowania symboli Emoji na tokeny znajduje się w osobnym pliku dokumentacji: [Dokumentacja tokenów](./docs/tokeny.md).

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

## Struktura projektu
* **`/src`** — kod źródłowy narzędzi: analizator leksykalny (`lexer.py`), analizator składniowy (`parser.py`), definicje emoji (`emoji_language.py`), skrypt eksportu do `.pas` (`emoji_to_pascal.py`), punkt wejścia wiersza poleceń (`main.py`).
* **`/docs`** — dokumentacja techniczna (m.in. spis tokenów).
* **`/examples`** — programy przykładowe w EmojiPascal (pliki z rozszerzeniem `.ep`).
* **`/output/pascal`** — domyślny katalog zapisu plików `.pas` generowanych przez `emoji_to_pascal.py` (gdy nie podano jawnej ścieżki wyjściowej).
* **`/output`** — (planowane) katalog na wygenerowany kod języka C po zaimplementowaniu emitera z AST.