# Dokumentacja Tokenów EmojiPascal

Ten dokument definiuje zestaw tokenów dla języka EmojiPascal (zakres mini-Pascal). Nazwy własne (zmienne) oraz napisy w cudzysłowach pozostają w formie tekstowej.

---

## 1. Słowa kluczowe (emoji)

| Nazwa tokenu | Symbol | Opis |
|:---|:---:|:---|
| `PROGRAM` | `🏁` | Nagłówek i początek programu |
| `VAR` | `📦` | Sekcja deklaracji zmiennych |
| `BEGIN` | `🚦` | Początek bloku instrukcji |
| `END` | `🛑` | Koniec bloku instrukcji |
| `IF` | `❓` | Instrukcja warunkowa |
| `THEN` | `➡️` | Początek gałęzi "prawda" |
| `ELSE` | `🙅` | Początek gałęzi "fałsz" |
| `WHILE` | `🔁` | Pętla warunkowa |
| `DO` | `▶️` | Początek ciała pętli |
| `PRINT` | `🖨️` | Wyświetlanie danych na wyjściu |

---

## 2. Typy danych

| Nazwa tokenu | Symbol | Opis |
|:---|:---:|:---|
| `TYPE_INT` | `🔢` | Typ całkowity (Integer) |
| `TYPE_STRING` | `🧵` | Typ tekstowy (String) |
| `TYPE_BOOL` | `✅` | Typ logiczny (Boolean) |

---

## 3. Operatory

| Nazwa tokenu | Symbol | Opis |
|:---|:---:|:---|
| `ASSIGN` | `⬅️` | Przypisanie (odpowiednik `:=`) |
| `PLUS` | `➕` | Dodawanie |
| `MINUS` | `➖` | Odejmowanie |
| `MUL` | `✖️` | Mnożenie |
| `DIV` | `➗` | Dzielenie |
| `EQ` | `🟰` | Równe |
| `NEQ` | `❌` | Różne |
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
| `DOT` | `.` | `🔚` | Znak końca programu |
| `LPAREN` | `(` | `🤜` | Nawias lewy |
| `RPAREN` | `)` | `🤛` | Nawias prawy |

---

## 5. Tokeny leksykalne i literały

W EmojiPascal literały liczbowe składają się z sekwencji cyfr w ramkach. Nazwy zmiennych oraz teksty pozostają w formie standardowej dla zapewnienia unikalności identyfikatorów.

| Kategoria | Format / Przykład | Opis |
|:---|:---|:---|
| `LITERAL_INT` | `0️⃣` do `9️⃣` | Cyfry emoji (np. `4️⃣``2️⃣` dla liczby 42) |
| `IDENTIFIER` | `x`, `suma_1` | Alfanumeryczne nazwy zmiennych |
| `LITERAL_STR` | `"Tekst"` | Napisy ujęte w cudzysłów |
| `LITERAL_BOOL` | `true`, `false` | Stałe logiczne |
| `COMMENT` | `// tekst` | Komentarze ignorowane przez parser |
| `WHITESPACE` | ` ` | Spacje, tabulatory, znaki nowej linii |
| `EOF` | `🔚` | Znacznik końca strumienia danych |