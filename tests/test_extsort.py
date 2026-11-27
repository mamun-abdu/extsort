import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "extsort.py"


def run(*args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args], capture_output=True, text=True
    )


class ExtsortTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def touch(self, rel, text="x"):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def test_sorts_by_lowercased_extension(self):
        self.touch("notes.txt")
        self.touch("Photo.JPG")
        self.touch("README")
        result = run(str(self.root))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.root / "txt" / "notes.txt").is_file())
        self.assertTrue((self.root / "jpg" / "Photo.JPG").is_file())
        self.assertTrue((self.root / "_no_ext" / "README").is_file())
        self.assertIn("Sorted 3 file(s).", result.stdout)

    def test_dry_run_moves_nothing(self):
        self.touch("report.pdf")
        result = run(str(self.root), "--dry-run")
        self.assertIn("would move: report.pdf -> pdf/", result.stdout)
        self.assertTrue((self.root / "report.pdf").is_file())
        self.assertFalse((self.root / "pdf").exists())

    def test_second_run_is_a_no_op(self):
        self.touch("a.csv")
        run(str(self.root))
        result = run(str(self.root))
        self.assertIn("Nothing to sort.", result.stdout)

    def test_existing_destination_is_skipped(self):
        self.touch("a.txt", "new")
        self.touch("txt/a.txt", "old")
        dry = run(str(self.root), "--dry-run")
        self.assertIn("would skip (exists)", dry.stderr)
        self.assertIn("Would sort 0 file(s).", dry.stdout)
        real = run(str(self.root))
        self.assertIn("skip (exists)", real.stderr)
        self.assertEqual((self.root / "txt" / "a.txt").read_text(), "old")
        self.assertEqual((self.root / "a.txt").read_text(), "new")

    def test_recursive_pulls_nested_files_up(self):
        self.touch("sub/deep/data.json")
        run(str(self.root), "--recursive")
        self.assertTrue((self.root / "json" / "data.json").is_file())

    def test_not_a_folder(self):
        result = run(str(self.root / "missing"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("Not a folder", result.stderr)


if __name__ == "__main__":
    unittest.main()
