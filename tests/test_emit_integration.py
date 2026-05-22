"""Transpilacja, kompilacja gcc i uruchomienie wybranych programow."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _run(cmd: list[str], *, cwd: Path = ROOT, input_text: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=cwd,
        input=input_text,
        capture_output=True,
        text=True,
    )


class TestEmitIntegration(unittest.TestCase):
    def setUp(self) -> None:
        if shutil.which("gcc") is None:
            self.skipTest("gcc niedostepny w PATH")

    def _emit_and_build(self, ep_name: str, binary_name: str) -> Path:
        ep = ROOT / "examples" / ep_name
        emit = _run([sys.executable, "src/main.py", "--emit-c", str(ep)])
        self.assertEqual(emit.returncode, 0, emit.stderr or emit.stdout)
        c_path = ROOT / "output" / "c" / f"{ep.stem}.c"
        self.assertTrue(c_path.is_file())

        out_dir = Path(tempfile.mkdtemp(prefix="emojipascal_test_"))
        self.addCleanup(lambda: shutil.rmtree(out_dir, ignore_errors=True))
        binary = out_dir / binary_name
        build = _run(["gcc", "-Wall", "-o", str(binary), str(c_path)])
        self.assertEqual(build.returncode, 0, build.stderr)
        return binary

    def test_suma_do_n(self) -> None:
        binary = self._emit_and_build("suma_do_n.ep", "suma")
        run = _run([str(binary)], input_text="5\n")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("15", run.stdout)

    def test_nwd(self) -> None:
        binary = self._emit_and_build("najwiekszy_wspolny_dzielnik.ep", "gcd")
        run = _run([str(binary)], input_text="48\n18\n")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("6", run.stdout)

    def test_test_ep_compiles(self) -> None:
        binary = self._emit_and_build("test.ep", "test")
        run = _run([str(binary)])
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("Koniec testu", run.stdout)

    def test_emit_contains_expected_fragments(self) -> None:
        _run([sys.executable, "src/main.py", "--emit-c", "examples/suma_do_n.ep"])
        c_src = (ROOT / "output" / "c" / "suma_do_n.c").read_text(encoding="utf-8")
        self.assertIn("scanf", c_src)
        self.assertIn("for (", c_src)
        self.assertIn("printf", c_src)


class TestSemanticFailure(unittest.TestCase):
    def test_undeclared_variable_blocks_emit(self) -> None:
        bad = ROOT / "examples" / "bad_niezadeklarowana.ep"
        result = _run([sys.executable, "src/main.py", "--emit-c", str(bad)])
        self.assertEqual(result.returncode, 4)
        self.assertIn("semantyczny", result.stderr.lower())


if __name__ == "__main__":
    unittest.main()
