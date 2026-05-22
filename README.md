EmojiPascal – Transpiler języka opartego na Pascalu na język C

## Dane autorów
* **Imię i Nazwisko:** Alicja Kwiatkowska 
  **E-mail:** kwiatkowskaa@student.agh.edu.pl
* **Imię i Nazwisko:** Dawid Kałucki
  **E-mail:** dkalucki@student.agh.edu.pl

---

## Szybki start

**Wymagania:** Python 3.10+, kompilator `gcc`, zależności z `requirements.txt`.

Wszystkie poniższe polecenia uruchamiaj z **katalogu głównego repozytorium** (tam, gdzie leżą `src/` i `examples/`).

```bash
pip install -r requirements.txt

# Suma liczb od 1 do n
python3 src/main.py --emit-c examples/suma_do_n.ep
gcc -Wall -o suma output/c/suma_do_n.c
printf "5\n" | ./suma
# Oczekiwany wynik: komunikaty + suma 15 (dla n=5)

# Największy wspólny dzielnik (Euklides)
python3 src/main.py --emit-c examples/najwiekszy_wspolny_dzielnik.ep
gcc -Wall -o gcd output/c/najwiekszy_wspolny_dzielnik.c
printf "48\n18\n" | ./gcd
# Oczekiwany wynik: NWD = 6
```

Ścieżka translacji: plik `.ep` → parser (AST) → `codegen_c.py` → plik `.c` → `gcc`. **Nie** trzeba generować pliku `.pas` po drodze.

---

## Założenia programu

### Ogólne cele programu
Celem projektu jest stworzenie narzędzia do translacji autorskiego języka opartego na składni Pascala, o nazwie **EmojiPascal**, w którym standardowe słowa kluczowe zostały zastąpione odpowiednimi symbolami Emoji. Projekt skupia się na praktycznej implementacji pełnego procesu konwersji: od odczytania znaków Emoji, przez analizę struktury programu, aż po wygenerowanie gotowego kodu w języku C.

### Rodzaj translatora
Program jest **transpilerem** — dokonuje translacji kodu źródłowego w języku **EmojiPascal** na **kod źródłowy w języku C** (język implementacji narzędzia to Python, co opisano poniżej).

### Planowany wynik działania programu
Docelowym wynikiem prac jest **transpiler** języka EmojiPascal do **kodu źródłowego w języku C**, gotowego do kompilacji przy użyciu kompilatora `gcc`.

**Stan realizacji (bieżący etap):** działa pełna ścieżka **lexer → parser (AST) → emiter C** (`codegen_c.py`, flaga `--emit-c`). Dwa programy z katalogu `examples/` można wygenerować do C, skompilować (`gcc`) i uruchomić — patrz [Szybki start](#szybki-start). Rozbudowa emitera pod pozostałe konstrukcje (m.in. `test.ep`: const, tablice, procedury, `case`) — w toku.

Osobno dostępny **skrypt pomocniczy** `emoji_to_pascal.py`: zamiana emoji na słowa Pascala i zapis `.pas` — to **podstawienie tekstowe**, nie etap pipeline’u do C.

| Plik w `examples/` | `--emit-c` + `gcc` + uruchomienie |
|:---|:---:|
| `suma_do_n.ep` | tak |
| `najwiekszy_wspolny_dzielnik.ep` | tak |
| `test.ep` | nie (jeszcze nieobsługiwane konstrukcje) |

### Język implementacji i środowisko
* **Python:** wersja **3.10 lub nowsza** (zalecana aktualna stabilna wersja interpretera).
* **Biblioteka PLY** (Python Lex–Yacc) — generator analizatorów leksykalnych i składniowych w oparciu o tablice **LALR**.

Instalacja zależności Pythona dla narzędzi w `src/`:

```bash
pip install -r requirements.txt
```

W pliku [`requirements.txt`](./requirements.txt) wymienione są pakiety zewnętrzne projektu. 

### Sposób realizacji skanera i parsera
W projekcie wykorzystywana jest biblioteka **PLY (Python Lex-Yacc)** — narzędzie implementujące mechanizmy analogiczne do Lex i Yacc w języku Python, umożliwiające formalne zdefiniowanie tokenów oraz reguł gramatyki.

PLY umożliwia w szczególności:
- implementację analizatora leksykalnego (lexer),
- implementację analizatora składniowego (parser),
- obsługę znaków Unicode (w tym emoji).

---

## Uruchomienie narzędzi

Polecenia wywołuj z **katalogu głównego repozytorium**. Ścieżkę do pliku `.ep` podaj względem tego katalogu (np. `examples/suma_do_n.ep`).

Interpreter Pythona **sam dodaje** do ścieżki importów folder `src/` przy `python3 src/main.py` — importy `lexer`, `parser`, `codegen_c` działają **bez** `PYTHONPATH`.

### Dwie niezależne ścieżki z pliku `.ep`

| Ścieżka | Narzędzie | Wynik |
|:---|:---|:---|
| **Główna (transpiler)** | `main.py --emit-c` | `output/c/*.c` → kompilacja `gcc` |
| **Pomocnicza (podgląd)** | `emoji_to_pascal.py` | `output/pascal/*.pas` (podstawienie emoji, bez AST) |

Łańcuch **`.ep` → `.pas` → `.c` nie istnieje** — do C idzie wyłącznie przez AST.

### Transpilacja do C i kompilacja

Po poprawnym sparsowaniu emiter zapisuje kod C; na stdout: `Zapisano: …`.

```bash
python3 src/main.py --emit-c ścieżka/do/programu.ep
gcc -Wall -o program output/c/nazwa_pliku.c
./program
```

* **Domyślny zapis:** `output/c/<nazwa_bez_rozszerzenia>.c`
* **Jawna ścieżka wyjściowa:** `python3 src/main.py --emit-c ścieżka/wyjście.c wejście.ep`

Programy z wejściem z klawiatury (`scanf`) uruchamiaj z danymi na stdin, np. `printf "5\n" | ./suma` — szczegóły w [Szybki start](#szybki-start).

Przy starcie parsera mogą pojawić się ostrzeżenia PLY o nieużywanym tokenie `RECORD` — można je zignorować.

### Tryby `main.py` (diagnostyka)

| Polecenie | Efekt | Plik wyjściowy |
|:---|:---|:---|
| `python3 src/main.py plik.ep` | lista tokenów na stdout | — |
| `python3 src/main.py --parse plik.ep` | drzewo AST na stdout | — |
| `python3 src/main.py --emit-c plik.ep` | generacja kodu C | `output/c/…` |

```bash
python3 src/main.py examples/suma_do_n.ep
python3 src/main.py --parse examples/suma_do_n.ep
```

Przykłady: katalog [`examples/`](./examples/).

### Eksport do pliku `.pas` (opcjonalnie)

Mapowanie symboli emoji → słowa Pascala (`src/emoji_language.py`). **Nie** korzysta z AST i **nie** służy do budowy pliku `.c`.

```bash
python3 src/emoji_to_pascal.py ścieżka/do/programu.ep
```

* **Domyślnie:** `output/pascal/<nazwa>.pas`
* **Jawnie:** `python3 src/emoji_to_pascal.py wejście.ep ścieżka/wyjście.pas`

### Rozwiązywanie problemów

| Problem | Co zrobić |
|:---|:---|
| `ModuleNotFoundError: ply` | `pip install -r requirements.txt` |
| `Blad skladni` / `Blad parsera` | porównaj `.ep` z działającymi przykładami w `examples/` |
| `NotImplementedError` przy `--emit-c` | konstrukcja jeszcze nieobsługiwana w emiterze (np. `test.ep`) |
| `gcc: command not found` | zainstaluj pakiet z kompilatorem C (np. `build-essential`) |
| Program „nic nie robi” / zły wynik | czy podajesz liczby na stdin (`printf "5\n" \| ./suma`) |

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

Uruchomienie tego programu po transpilacji: [Szybki start](#szybki-start) (sekcja NWD).

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
* **`/src`** — `lexer.py`, `parser.py`, `codegen_c.py` (emiter C), `emoji_language.py`, `emoji_to_pascal.py`, `main.py` (CLI: tokeny, `--parse`, `--emit-c`).
* **`/docs`** — dokumentacja techniczna (m.in. [tokeny](./docs/tokeny.md)).
* **`/examples`** — programy `.ep` (źródła do testów transpilera).
* **`/output/c`** — wygenerowane pliki `.c` (`--emit-c`); można commitować jako referencję lub generować lokalnie.
* **`/output/pascal`** — wygenerowane `.pas` (`emoji_to_pascal.py`), niezależnie od ścieżki do C.