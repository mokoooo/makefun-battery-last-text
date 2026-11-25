#!/usr/bin/env python3
"""The Battery's Last Text to Its Charger — a one-line make.fun entry.

When executed, this module delivers exactly one farewell text from a
dying phone battery to the charger it waited for all day. The harness
expects that text in entry.txt inside the directory named by the
MAKEFUN_OUTPUT_DIR environment variable (defaulting to /output).
"""

import os
import tempfile
from pathlib import Path

FINAL_TEXT = (
    "At 1% I dimmed my screen, killed my apps and saved myself all day "
    "for you — so when you finally plug in, at least act shocked."
)
LIMIT = 200


def validate(text: str) -> None:
    """Refuse any farewell the sealed gate would mark invalid."""
    if not text or len(text) > LIMIT:
        raise ValueError("farewell must be between 1 and 200 characters")
    if text.strip() != text or not text.strip():
        raise ValueError("farewell must be a single trimmed line")
    if len(text.splitlines()) != 1:
        raise ValueError("farewell must stay on one line")


def render() -> str:
    """Return the farewell text after validation."""
    validate(FINAL_TEXT)
    return FINAL_TEXT


def destination() -> Path:
    """Pick the output directory, tolerating padded environment values."""
    chosen = os.getenv("MAKEFUN_OUTPUT_DIR", "").strip()
    return Path(chosen or "/output")


def deliver() -> Path:
    """Write entry.txt atomically inside the destination directory."""
    folder = destination()
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / "entry.txt"
    handle = tempfile.NamedTemporaryFile(
        mode="wb", dir=folder, prefix=".farewell-", delete=False
    )
    temp_path = Path(handle.name)
    try:
        with handle:
            handle.write((render() + "\n").encode("utf-8"))
        os.chmod(temp_path, 0o644)
        temp_path.replace(target)
    except BaseException:
        temp_path.unlink(missing_ok=True)
        raise
    return target


def main() -> int:
    deliver()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
