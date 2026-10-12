"""One-off, hash-guarded fix applied after the gap-filling write of 3 Oct 2026.

Replaces the caption "(nominal \\$)" of the §D8 SBIR period table with "(nominal US dollars)",
because the PDF checker flags a lone dollar sign in running text. The expected report hash
before the fix is the one written by apply_gapfill.py (453a99a75c9e...).

Usage:
    python fix_caption_dollar.py
"""
import hashlib
from pathlib import Path

p = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
raw = p.read_bytes()
h = hashlib.sha256(raw).hexdigest()
assert h.startswith("453a99a75c9e"), h
t = raw.decode("utf-8")
old = r"**US lidar SBIR/STTR awards, annual averages by period** (nominal \$)"
assert t.count(old) == 1, t.count(old)
t2 = t.replace(old, "**US lidar SBIR/STTR awards, annual averages by period** (nominal US dollars)")
assert hashlib.sha256(p.read_bytes()).hexdigest() == h, "report changed during processing"
p.write_bytes(t2.encode("utf-8"))
print("written", hashlib.sha256(t2.encode("utf-8")).hexdigest()[:12])
