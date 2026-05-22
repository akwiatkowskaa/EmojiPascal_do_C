#!/usr/bin/env bash
# Demo transpilera EmojiPascal -> C (uruchom z katalogu glownego repozytorium).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if ! command -v gcc >/dev/null 2>&1; then
  echo "Brak gcc w PATH" >&2
  exit 1
fi

echo "=== suma_do_n.ep ==="
python3 src/main.py --emit-c examples/suma_do_n.ep
gcc -Wall -o /tmp/emojipascal_suma output/c/suma_do_n.c
printf "5\n" | /tmp/emojipascal_suma

echo ""
echo "=== najwiekszy_wspolny_dzielnik.ep ==="
python3 src/main.py --emit-c examples/najwiekszy_wspolny_dzielnik.ep
gcc -Wall -o /tmp/emojipascal_gcd output/c/najwiekszy_wspolny_dzielnik.c
printf "48\n18\n" | /tmp/emojipascal_gcd

echo ""
echo "=== test.ep ==="
python3 src/main.py --emit-c examples/test.ep
gcc -Wall -o /tmp/emojipascal_test output/c/test.c
/tmp/emojipascal_test

echo ""
echo "Demo zakonczone pomyslnie."
