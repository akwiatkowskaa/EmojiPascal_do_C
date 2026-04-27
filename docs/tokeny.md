# Dokumentacja Tokenów EmojiPascal

Ten dokument definiuje zestaw tokenow dla jezyka EmojiPascal (zakres mini-Pascal). Nazwy wlasne (zmienne) oraz napisy w cudzyslowach pozostaja w formie tekstowej.

---

## 0. Najwazniejsze tokeny uzywane w parserze (MVP)

| Obszar | Token | Emoji | Zastosowanie |
|:---|:---|:---:|:---|
| Struktura programu | `PROGRAM`, `BEGIN`, `END`, `DOT` | `🏁`, `🚦`, `🛑`, `🔚` | Szkielet programu i blokow |
| Deklaracje | `VAR`, `COLON`, `SEMICOLON`, `COMMA` | `📦`, `📍`, `🔹`, `📎` | Definicje zmiennych i listy identyfikatorow |
| Typy | `TYPE_INT`, `TYPE_REAL`, `TYPE_BOOL`, `TYPE_STRING` | `🔢`, `🌊`, `✅`, `🧵` | Podstawowe typy danych |
| Przypisanie i arytmetyka | `ASSIGN`, `PLUS`, `MINUS`, `MUL`, `DIV`, `MOD` | `⬅️`, `➕`, `➖`, `✖️`, `➗`, `✂️` | Operacje obliczeniowe |
| Relacje i logika | `EQ`, `NEQ`, `LT`, `LE`, `GT`, `GE`, `AND`, `OR`, `NOT` | `🟰`, `❌`, `🔽`, `⏬`, `🔼`, `⏫`, `🤝`, `🔀`, `🚫` | Warunki i wyrazenia logiczne |
| Sterowanie | `IF`, `THEN`, `ELSE`, `WHILE`, `DO`, `FOR`, `TO` | `❓`, `➡️`, `🙅`, `🔁`, `▶️`, `🔂`, `⬆️` | Instrukcje sterujace |
| Wywolania | `LPAREN`, `RPAREN` | `🤜`, `🤛` | Argumenty funkcji/procedur |

---

## 1. Slowa kluczowe

| Nazwa tokenu | Symbol | Opis |
|:---|:---:|:---|
| `PROGRAM` | `🏁` | Nagłówek i początek programu |
| `CONST` | `📌` | Sekcja stalych |
| `VAR` | `📦` | Sekcja deklaracji zmiennych |
| `FUNCTION` | `⚙️` | Definicja nowej funkcji (podprogramu) |
| `PROCEDURE` | `🔧` | Definicja procedury (bez zwracania wartosci) |
| `BEGIN` | `🚦` | Początek bloku instrukcji |
| `END` | `🛑` | Koniec bloku instrukcji |
| `RETURN` | `↩️` | Zwrócenie wartości z funkcji |
| `IF` | `❓` | Instrukcja warunkowa |
| `THEN` | `➡️` | Początek gałęzi "prawda" |
| `ELSE` | `🙅` | Początek gałęzi "fałsz" |
| `WHILE` | `🔁` | Pętla warunkowa |
| `DO` | `▶️` | Początek ciała pętli |
| `REPEAT` | `🔁🔂` | Petla z warunkiem na koncu |
| `UNTIL` | `🔂▶️` | Warunek zakonczenia petli `repeat` |
| `FOR` | `🔂` | Petla iteracyjna |
| `TO` | `⬆️` | Rosnacy zakres petli `for` |
| `DOWNTO` | `⬇️` | Malejacy zakres petli `for` |
| `CASE` | `🧭` | Instrukcja wyboru |
| `OF` | `🧾` | Uzywane w `array ... of ...` oraz `case ... of` |
| `ARRAY` | `📚` | Typ tablicowy |
| `RECORD` | `🧱` | Typ rekordowy |
| `IN` | `📥➡️` | Test przynaleznosci (opcjonalnie) |
| `PRINT` | `🖨️` | Wyświetlanie danych na wyjściu |
| `INPUT` | `📥` | Pobieranie danych od użytkownika |

---

## 2. Typy danych

| Nazwa tokenu | Symbol | Opis |
|:---|:---:|:---|
| `TYPE_INT` | `🔢` | Typ całkowity (Integer) |
| `TYPE_REAL` | `🌊` | Typ rzeczywisty (Real) |
| `TYPE_STRING` | `🧵` | Typ tekstowy (String) |
| `TYPE_BOOL` | `✅` | Typ logiczny (Boolean) |
| `TYPE_CHAR` | `🔡` | Typ znakowy (Char) |
| `TYPE_ARRAY` | `📚` | Typ tablicowy (wymaga rozmiaru w nawiasach) |
| `TYPE_RECORD` | `🧱` | Typ rekordowy |

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
| `RANGE` | `↔️` | Zakres (np. indeksy tablic) |
| `FIELD_ACCESS` | `💠` | Dostep do pola rekordu |

---

## 4. Separatory i znaki specjalne

| Nazwa tokenu | Klasyczny Pascal | Emoji | Opis |
|:---|:---:|:---:|:---|
| `SEMICOLON` | `;` | `🔹` | Separator instrukcji |
| `COLON` | `:` | `📍` | Separator typu w deklaracjach |
| `COMMA` | `,` | `📎` | Separator identyfikatorów |
| `DOT` | `.` | `🔚` | Koniec programu (`program ... .`) |
| `LPAREN` | `(` | `🤜` | Nawias lewy / Indeksowanie tablic |
| `RPAREN` | `)` | `🤛` | Nawias prawy / Indeksowanie tablic |
| `BYREF` | `var` | `📤` | Parametr przekazywany przez referencje |
| `LBRACKET` | `[` | `🫲` | Nawias kwadratowy lewy (opcjonalnie) |
| `RBRACKET` | `]` | `🫱` | Nawias kwadratowy prawy (opcjonalnie) |

---

## 5. Tokeny leksykalne i literały

W EmojiPascal literały liczbowe składają się z sekwencji cyfr w ramkach. Nazwy zmiennych oraz teksty pozostają w formie tekstowej dla zapewnienia unikalności identyfikatorów.

| Kategoria | Format / Przykład | Opis |
|:---|:---|:---|
| `LITERAL_INT` | `0️⃣` do `9️⃣` | Cyfry emoji (np. `4️⃣2️⃣` dla liczby 42) |
| `LITERAL_REAL` | `3️⃣.1️⃣4️⃣` | Liczby rzeczywiste |
| `IDENTIFIER` | `x`, `suma_1` | Alfanumeryczne nazwy zmiennych |
| `LITERAL_STR` | `"Tekst"` | Napisy ujęte w cudzysłów |
| `LITERAL_CHAR` | `'A'` | Znak pojedynczy |
| `LITERAL_BOOL` | `true`, `false` | Stałe logiczne |
| `COMMENT` | `//`, `{...}`, `(*...*)` | Komentarze ignorowane przez parser |
| `WHITESPACE` | ` ` | Spacje, tabulatory, znaki nowej linii |
| `EOF` | *(brak symbolu)* | Koniec strumienia wejscia (generowany przez lexer) |

---

## 6. Ustalenia skladniowe (zeby gramatyka byla spojna)

- `program` ma postac: `🏁 identyfikator 🔹 <block> 🔚`.
- `<block>`: opcjonalnie `const`, opcjonalnie `var`, zero lub wiecej podprogramow, potem `🚦 ... 🛑`.
- Wyrazenia sa warstwowe (od najnizszego priorytetu): `or` -> `and` -> relacje -> `+/-` -> `*//mod` -> unarne.
- Funkcje i procedury moga miec pusta liste parametrow.
- `case` i `repeat-until` sa przewidziane jako elementy etapu rozszerzonego.

## 7. Minimalny zakres wdrozenia (MVP)

1. Tokeny podstawowe: deklaracje, przypisanie, wyrazenia, `if`, `while`, `for`, funkcja/procedura.
2. Typy podstawowe: `int`, `real`, `bool`, `string`.
3. Dodatki po MVP: `record`, `case`, pelne wsparcie indeksowania i dostepu do pol.