#!/usr/bin/env python3
"""
Small helper to insert a short license header into source files.
Use with care: it will skip files that already contain the header.
"""
import sys
from pathlib import Path

HEADER = """# Copyright (c) 2025 Pulast Tiwari
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
"""

EXTS = {".py", ".js", ".jsx", ".ts", ".tsx"}


def insert_header(path: Path):
    text = path.read_text(encoding="utf-8")
    if HEADER.strip() in text:
        return False
    if path.suffix not in EXTS:
        return False
    # naive insertion after shebang if present
    if text.startswith("#!/"):
        parts = text.splitlines(True)
        shebang = parts[0]
        rest = "".join(parts[1:])
        new = shebang + HEADER + "\n" + rest
    else:
        new = HEADER + "\n" + text
    path.write_text(new, encoding="utf-8")
    return True


if __name__ == "__main__":
    root = Path(".")
    changed = []
    for p in root.rglob("*"):
        if p.is_file():
            try:
                if insert_header(p):
                    changed.append(str(p))
            except Exception:
                pass
    if changed:
        print("Inserted header into:")
        print("\n".join(changed))
    else:
        print("No files changed")
