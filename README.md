EmojiPascal – Transpiler języka opartego na Pascalu na język C

## Dane autorów
* **Imię i Nazwisko:** Alicja Kwiatkowska 
  **E-mail:** kwiatkowskaa@student.agh.edu.pl
* **Imię i Nazwisko:** Dawid Kałucki
  **E-mail:** 

---

## Założenia programu

### Ogólne cele programu
Celem projektu jest stworzenie narzędzia do translacji autorskiego języka opartego na składni Pascala, o nazwie **EmojiPascal**, w którym standardowe słowa kluczowe zostały zastąpione odpowiednimi symbolami Emoji. Projekt skupia się na praktycznej implementacji pełnego procesu konwersji: od odczytania znaków Emoji, przez analizę struktury programu, aż po wygenerowanie gotowego kodu w języku C.

### Rodzaj translatora
Program jest **konwerterem (transpilerem)**, który dokonuje translacji kodu źródłowego wysokiego poziomu na inny kod źródłowy wysokiego poziomu.

### Planowany wynik działania programu
Kompilator (transpiler) języka **EmojiPascal do kodu źródłowego języka C**. Kod wynikowy będzie gotowy do bezpośredniej kompilacji przy użyciu kompilatora `gcc`.

### Planowany język implementacji
* **Python 3.13** <!--?? -->

### Sposób realizacji skanera/parsera
Do realizacji analizy leksykalnej i składniowej zostanie wykorzystany generator parserów...  <!--?? -->
---

## Struktura projektu
* `/src` – kod źródłowy transpilera (Lexer, Parser, Generator kodu).
* `/docs` – dokumentacja techniczna, spis tokenów oraz gramatyka projektu.
* `/examples` – przykładowe programy w języku EmojiPascal (pliki `.ep`).  <!--albo inne rozszerzenie -->
* `/output` – wygenerowane pliki źródłowe w języku C.