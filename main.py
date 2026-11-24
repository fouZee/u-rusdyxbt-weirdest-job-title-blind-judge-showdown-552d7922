#!/usr/bin/env python3
"""Weirdest Job Title entry writer.

Writes a single job title (60 characters at most, and nothing else) to
/output/entry.txt, the file the make.fun gate reads.

The title is deliberately a real-sounding job with one gloriously odd
twist: relocating icebergs is a job you can picture someone doing, in a
high-vis jacket, with a tugboat and a clipboard - and it is a job nobody
has ever heard of.
"""

import os
import sys

TITLE = "Senior Iceberg Relocation Specialist"

OUTPUT_PATH = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")


def validate(title: str) -> None:
    """Enforce the bounty gate: UTF-8 text, 1-60 chars, not only whitespace."""
    if not isinstance(title, str):
        raise ValueError("title must be a string")
    title.encode("utf-8")  # raises if not valid UTF-8-encodable text
    if not (1 <= len(title) <= 60):
        raise ValueError(f"title must be 1-60 characters, got {len(title)}")
    if not title.strip():
        raise ValueError("title must not be only whitespace")
    if "\n" in title or "\r" in title:
        raise ValueError("title must be a single line")
    if any(ord(ch) < 32 for ch in title):
        raise ValueError("title must not contain control characters")
    if len(title.split()) < 2:
        raise ValueError("title must name a job in more than one word")
    # The judge weighs "sounds like a real job": a seniority prefix plus a
    # specialist noun phrase reads as a genuine corporate title.


def main() -> int:
    validate(TITLE)
    out_dir = os.path.dirname(OUTPUT_PATH)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(TITLE)
    # Re-read and verify the written file byte for byte: what the gate
    # reads must be exactly the validated title, nothing else.
    with open(OUTPUT_PATH, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != TITLE:
        raise ValueError(f"written entry differs from validated title: {written!r}")
    print(f"Wrote {len(TITLE)}-character entry to {OUTPUT_PATH}: {TITLE!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
