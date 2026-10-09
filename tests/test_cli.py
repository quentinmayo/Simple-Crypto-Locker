import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from wild_bat.cli import main

ROOT = Path(__file__).resolve().parents[1]


class CliTests(unittest.TestCase):
    def test_json_output_is_a_single_report(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = main(["demo", "--scenario", "containment", "--documents", "4", "--format", "json"])
        self.assertEqual(result, 0)
        self.assertEqual(json.loads(output.getvalue())["summary"]["untouched"], 3)

    def test_text_output_labels_simulation(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(["demo"]), 0)
        self.assertIn("SIMULATION ONLY", output.getvalue())
        self.assertIn("restored=3", output.getvalue())

    def test_lists_all_scenarios(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(["scenarios"]), 0)
        for name in ("recovery", "containment", "no-backup"):
            self.assertIn(name, output.getvalue())

    def test_invalid_arguments_use_exit_code_two(self):
        cases = ([], ["demo", "--documents", "0"], ["demo", "--documents", "1001"],
                 ["demo", "--documents", "abc"], ["demo", "--scenario", "unknown"],
                 ["demo", "--path", "/tmp"], ["demo", "--format", "xml"])
        for args in cases:
            with self.subTest(args=args), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as caught:
                    main(args)
                self.assertEqual(caught.exception.code, 2)

    def test_help_and_version_exit_successfully(self):
        for args in (["--help"], ["--version"], ["demo", "--help"]):
            with self.subTest(args=args), contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(SystemExit) as caught:
                    main(args)
                self.assertEqual(caught.exception.code, 0)

    def test_module_runs_from_unrelated_directory_without_touching_document(self):
        with tempfile.TemporaryDirectory() as directory:
            sentinel = Path(directory) / "personal-document.txt"
            sentinel.write_bytes(b"Keep this document unchanged.\x00")
            env = dict(os.environ, PYTHONPATH=str(ROOT), PYTHONDONTWRITEBYTECODE="1")
            for scenario in ("recovery", "containment", "no-backup"):
                result = subprocess.run(
                    [sys.executable, "-m", "wild_bat", "demo", "--scenario", scenario, "--format", "json"],
                    cwd=directory, env=env, capture_output=True, text=True, timeout=10,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIs(json.loads(result.stdout)["simulation"], True)
                self.assertEqual(sentinel.read_bytes(), b"Keep this document unchanged.\x00")
                self.assertEqual(list(Path(directory).iterdir()), [sentinel])

    def test_legacy_entry_points_refuse_to_run(self):
        for name in ("HW1.py", "server.py"):
            with self.subTest(name=name):
                result = subprocess.run([sys.executable, str(ROOT / name)], capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, 1)
                self.assertIn("retired", result.stderr)

    def test_legacy_entry_points_are_inert_on_import(self):
        for name in ("HW1.py", "server.py"):
            with self.subTest(name=name), contextlib.redirect_stdout(io.StringIO()) as out:
                spec = importlib.util.spec_from_file_location("legacy_stub", ROOT / name)
                spec.loader.exec_module(importlib.util.module_from_spec(spec))
                self.assertEqual(out.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
