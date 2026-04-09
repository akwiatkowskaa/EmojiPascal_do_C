# EmojiPascal Token List

This document defines the token set for EmojiPascal (mini-Pascal scope).
Identifiers remain textual and string literal contents are preserved as written.

---

## 1) Keywords (emoji-based)

| Token Name | Symbol | Description |
|---|---|---|
| `PROGRAM` | `🏁` | Program start/header keyword |
| `VAR` | `📦` | Variable declaration section |
| `BEGIN` | `🚦` | Start of executable block |
| `END` | `🛑` | End of block |
| `IF` | `❓` | Conditional statement |
| `THEN` | `➡️` | Starts IF true branch |
| `ELSE` | `🙅` | Starts IF false branch |
| `WHILE` | `🔁` | While loop |
| `DO` | `▶️` | Starts WHILE body |
| `PRINT` | `🖨️` | Output statement |

---

## 2) Type Tokens

| Token Name | Symbol | Description |
|---|---|---|
| `TYPE_INT` | `🔢` | Integer type |
| `TYPE_STRING` | `🧵` | String type |
| `TYPE_BOOL` | `✅` | Boolean type |

---

## 3) Operators (emoji variants)

| Token Name | Symbol | Description |
|---|---|---|
| `ASSIGN` | `⬅️` | Assignment (Pascal `:=` equivalent) |
| `PLUS` | `➕` | Addition |
| `MINUS` | `➖` | Subtraction |
| `MUL` | `✖️` | Multiplication |
| `DIV` | `➗` | Division |
| `EQ` | `🟰` | Equal comparison |
| `NEQ` | `❌` | Not-equal comparison |
| `LT` | `🔽` | Less-than |
| `LE` | `⏬` | Less-than-or-equal |
| `GT` | `🔼` | Greater-than |
| `GE` | `⏫` | Greater-than-or-equal |
| `AND` | `🤝` | Logical AND |
| `OR` | `🔀` | Logical OR |
| `NOT` | `🚫` | Logical NOT |

---

## 4) Symbolic Delimiters as Emojis

| Token Name | Classic Pascal Symbol | Emoji Form (Proposed) | Description |
|---|---|---|---|
| `SEMICOLON` | `;` | `🔹` | Statement separator |
| `COLON` | `:` | `📍` | Type separator in declarations |
| `COMMA` | `,` | `📎` | Identifier separator |
| `DOT` | `.` | `🛑.` or `🏁.` | Program terminator marker (proposal) |
| `LPAREN` | `(` | `🤜` | Left parenthesis (optional emoji mode) |
| `RPAREN` | `)` | `🤛` | Right parenthesis (optional emoji mode) |

---

## 5) Standard Lexical Tokens (remain textual)

| Token Name | Example | Description |
|---|---|---|
| `IDENTIFIER` | `x`, `sum`, `counter_1` | Variable names, unchanged text |
| `NUMBER` | `0`, `42`, `1000` | Integer literal |
| `STRING` | `"Hello"` | String literal, content unchanged |
| `BOOL_LITERAL` | `true`, `false` | Boolean literal |
| `COMMENT` | `// note` | Single-line comment |
| `WHITESPACE` | space/tab/newline | Ignored except for positions |
| `EOF` | end-of-file | Internal lexer token |


