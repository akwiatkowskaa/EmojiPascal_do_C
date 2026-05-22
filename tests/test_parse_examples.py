"""Wszystkie przyklady .ep (poza celowo blednymi) musza przejsc parser."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


class TestParseExamples(unittest.TestCase):
    def test_each_example_parses(self) -> None:
        from parser import parse_source

        examples = sorted((ROOT / "examples").glob("*.ep"))
        self.assertGreater(len(examples), 0)
        for path in examples:
            if path.name.startswith("bad_"):
                continue
            with self.subTest(path=path.name):
                tree = parse_source(path.read_text(encoding="utf-8"))
                self.assertIsNotNone(tree)
                self.assertEqual(tree[0], "Program")


if __name__ == "__main__":
    unittest.main()
