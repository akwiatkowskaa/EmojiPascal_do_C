# Dokumentacja Tokenów EmojiPascal

Ten dokument definiuje zestaw tokenów dla języka EmojiPascal (zakres mini-Pascal). Nazwy własne (zmienne) oraz napisy w cudzysłowach pozostają w formie tekstowej.

---

## 1. Słowa kluczowe

| Nazwa tokenu | Symbol | Opis |
|:---|:---:|:---|
| `PROGRAM` | `🏁` | Nagłówek i początek programu |
| `VAR` | `📦` | Sekcja deklaracji zmiennych |
| `FUNCTION` | `⚙️` | Definicja nowej funkcji (podprogramu) |
| `BEGIN` | `🚦` | Początek bloku instrukcji |
| `END` | `🛑` | Koniec bloku instrukcji |
| `RETURN` | `↩️` | Zwrócenie wartości z funkcji |
| `IF` | `❓` | Instrukcja warunkowa |
| `THEN` | `➡️` | Początek gałęzi "prawda" |
| `ELSE` | `🙅` | Początek gałęzi "fałsz" |
| `WHILE` | `🔁` | Pętla warunkowa |
| `DO` | `▶️` | Początek ciała pętli |
| `PRINT` | `🖨️` | Wyświetlanie danych na wyjściu |
| `INPUT` | `📥` | Pobieranie danych od użytkownika |

---

## 2. Typy danych

| Nazwa tokenu | Symbol | Opis |
|:---|:---:|:---|
| `TYPE_INT` | `🔢` | Typ całkowity (Integer) |
| `TYPE_STRING` | `🧵` | Typ tekstowy (String) |
| `TYPE_BOOL` | `✅` | Typ logiczny (Boolean) |
| `TYPE_ARRAY` | `📚` | Typ tablicowy (wymaga rozmiaru w nawiasach) |

---

## 3. Operatory

| Nazwa tokenu | Symbol | Opis |
|:---|:---:|:---|
| `ASSIGN` | `⬅️` | Przypisanie (odpowiednik `:=`) |
| `CAST` | `✨` | Magiczna konwersja typu (rzutowanie) |
| `PLUS` | `➕` | Dodawanie |
| `MINUS` | `➖` | Odejmowanie |
| `MUL` | `✖️` | Mnożenie |
| `DIV` | `➗` | Dzielenie |
| `EQ` | `🟰` | Równe |
| `NEQ` | `❌` | Różne |
| `MOD` | `✂️` | Reszta z dzielenia (Modulo) |
| `LT` | `🔽` | Mniejsze niż |
| `LE` | `⏬` | Mniejsze lub równe |
| `GT` | `🔼` | Większe niż |
| `GE` | `⏫` | Większe lub równe |
| `AND` | `🤝` | Koniunkcja logiczna |
| `OR` | `🔀` | Alternatywa logiczna |
| `NOT` | `🚫` | Negacja logiczna |

---

## 4. Separatory i znaki specjalne

| Nazwa tokenu | Klasyczny Pascal | Emoji | Opis |
|:---|:---:|:---:|:---|
| `SEMICOLON` | `;` | `🔹` | Separator instrukcji |
| `COLON` | `:` | `📍` | Separator typu w deklaracjach |
| `COMMA` | `,` | `📎` | Separator identyfikatorów |
| `DOT` | `.` | `🔚` | Znak końca programu / EOF |
| `LPAREN` | `(` | `🤜` | Nawias lewy / Indeksowanie tablic |
| `RPAREN` | `)` | `🤛` | Nawias prawy / Indeksowanie tablic |

---

## 5. Tokeny leksykalne i literały

W EmojiPascal literały liczbowe składają się z sekwencji cyfr w ramkach. Nazwy zmiennych oraz teksty pozostają w formie tekstowej dla zapewnienia unikalności identyfikatorów.

| Kategoria | Format / Przykład | Opis |
|:---|:---|:---|
| `LITERAL_INT` | `0️⃣` do `9️⃣` | Cyfry emoji (np. `4️⃣2️⃣` dla liczby 42) |
| `IDENTIFIER` | `x`, `suma_1` | Alfanumeryczne nazwy zmiennych |
| `LITERAL_STR` | `"Tekst"` | Napisy ujęte w cudzysłów |
| `LITERAL_BOOL` | `true`, `false` | Stałe logiczne |
| `COMMENT` | `// tekst` | Komentarze ignorowane przez parser |
| `WHITESPACE` | ` ` | Spacje, tabulatory, znaki nowej linii |
| `EOF` | `🔚` | Znacznik końca strumienia danych |