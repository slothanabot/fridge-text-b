#!/usr/bin/env python3
"""The 3AM Fridge Text — account B entry.

A smart fridge texts its owner at 3am. One line, one voice, no follow-up.
The program writes the text to /output/entry.txt.

Gate (sealed scorer): /output/entry.txt must be UTF-8 text of 1-140
characters, not only white space. This program enforces that itself
before and after writing, so a bad line can never reach the gate.
"""

import os
import sys

# The line: a concrete absurd 3am scene, in the fridge's own small voice.
# Fresh angle (no milk, no ice, no door left open): the leftovers have
# organised, and the fridge is caught in the middle of it.
ENTRY = "3am. The leftovers have unionised and want a microwave. I said you're asleep. They saw the light."

MAX_CHARS = 140
OUT_PATH = "/output/entry.txt"


def gate(text: str) -> str:
    """Return the entry if it passes the gate, else raise ValueError."""
    if not isinstance(text, str):
        raise ValueError("entry is not text")
    text = text.strip()
    if not text:
        raise ValueError("entry is empty or only white space")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} chars, over the {MAX_CHARS} cap"
        )
    # Must round-trip as clean UTF-8 with no stray control characters.
    raw = text.encode("utf-8")
    if raw.decode("utf-8") != text:
        raise ValueError("entry does not round-trip as UTF-8")
    if any(ord(ch) < 0x20 for ch in text):
        raise ValueError("entry holds control characters")
    return text


def main() -> int:
    try:
        text = gate(ENTRY)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    # Write with no trailing newline: the gate counts every character.
    with open(OUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    # Verify what landed on disk, byte for byte, before reporting success.
    with open(OUT_PATH, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != text:
        print("error: written file does not match the entry", file=sys.stderr)
        return 1
    if gate(written) != text:
        print("error: written file fails the gate", file=sys.stderr)
        return 1
    print(f"wrote {len(text)} chars to {OUT_PATH}")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
