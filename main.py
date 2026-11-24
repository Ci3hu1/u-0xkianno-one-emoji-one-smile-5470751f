#!/usr/bin/env python3
"""One Emoji, One Smile entry.

Writes exactly one emoji — 🥹 — to /output/entry.txt, nothing else.
Pure standard library. Deterministic: the same bytes on every run.
The gate: /output/entry.txt must be UTF-8 text of 1 to 8 characters,
not only white space.
"""

import os
from pathlib import Path

EMOJI = "🥹"

OUTPUT_PATH = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")


def main() -> None:
    if not (1 <= len(EMOJI) <= 8):
        raise ValueError(f"entry must be 1-8 characters, got {len(EMOJI)}")
    if not EMOJI.strip():
        raise ValueError("entry must not be only white space")
    # The grader collects outputs as another user: make sure anything we
    # create (the /output directory as well as the file) is world-readable.
    os.umask(0o022)
    out_dir = os.path.dirname(OUTPUT_PATH) or "."
    os.makedirs(out_dir, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(EMOJI)
    # Self-check: the file must hold exactly the emoji, nothing else.
    if Path(OUTPUT_PATH).read_text(encoding="utf-8") != EMOJI:
        raise ValueError("entry file does not hold exactly the emoji")
    # The grader collects outputs as another user: leave the file
    # world-readable (a tempfile/mkstemp default of 0600 fails the gate).
    os.chmod(OUTPUT_PATH, 0o644)


if __name__ == "__main__":
    main()
