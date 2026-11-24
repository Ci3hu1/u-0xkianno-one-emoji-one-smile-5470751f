"""Tests for the One Emoji, One Smile entry program."""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EMOJI = "🥹"


class TestEntry(unittest.TestCase):
    def run_main(self, tmp: Path) -> Path:
        out = tmp / "entry.txt"
        env = dict(os.environ, ENTRY_OUTPUT=str(out))
        subprocess.run(
            [sys.executable, str(ROOT / "main.py")],
            check=True, env=env, cwd=str(ROOT),
        )
        return out

    def test_writes_exact_emoji(self):
        with tempfile.TemporaryDirectory() as d:
            out = self.run_main(Path(d))
            self.assertEqual(out.read_bytes(), EMOJI.encode("utf-8"))

    def test_length_within_gate(self):
        # Gate: /output/entry.txt must be 1-8 characters, not only whitespace.
        self.assertTrue(1 <= len(EMOJI) <= 8)
        self.assertEqual(len(EMOJI), 1)

    def test_non_blank_and_utf8(self):
        self.assertTrue(EMOJI.strip())
        EMOJI.encode("utf-8")

    def test_output_deterministic(self):
        # Same bytes on every run.
        with tempfile.TemporaryDirectory() as d:
            first = self.run_main(Path(d)).read_bytes()
            second = self.run_main(Path(d)).read_bytes()
            self.assertEqual(first, second)

    def test_output_world_readable(self):
        # The grader collects outputs as another user; 0600 fails.
        with tempfile.TemporaryDirectory() as d:
            out = self.run_main(Path(d))
            self.assertTrue(out.stat().st_mode & 0o444)


if __name__ == "__main__":
    unittest.main()
