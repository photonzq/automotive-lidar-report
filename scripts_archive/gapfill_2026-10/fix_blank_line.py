"""One-off, hash-guarded fix after the third gap-filling batch of 3 Oct 2026.

The EU defence block of §D8 was inserted without a blank line before "**US: how the count was made**",
so pandoc ran that heading line into the last bullet of the block. This inserts the blank line.
Expected report hash before the fix: 551411dcc8fa...

Usage:
    python fix_blank_line.py
"""
import hashlib
from pathlib import Path

p = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
raw = p.read_bytes()
h = hashlib.sha256(raw).hexdigest()
assert h.startswith("551411dcc8fa"), h
lines = raw.decode("utf-8").split("\n")
idx = [i for i, l in enumerate(lines) if l.startswith("**US: how the count was made** [E unless tagged]")]
assert len(idx) == 1, idx
i = idx[0]
assert lines[i - 1].startswith("- **Other EU signals.**"), lines[i - 1][:60]
lines.insert(i, "")
out = "\n".join(lines).encode("utf-8")
assert hashlib.sha256(p.read_bytes()).hexdigest() == h, "report changed during processing"
p.write_bytes(out)
print("written", hashlib.sha256(out).hexdigest()[:12])
