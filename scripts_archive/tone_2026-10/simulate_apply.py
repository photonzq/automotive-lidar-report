"""Apply a list of edit pairs to a copy of a text file, in order, and report any that fail.

Each pair is {"id", "old", "new"} with an optional "expect" (number of occurrences, default 1, all replaced).
At its turn, each "old" must occur exactly "expect" times in the text as already edited; otherwise the pair
is reported and skipped. With --write OUT the edited text is saved to OUT (the source is never touched).

Usage: python simulate_apply.py <source> <pairs.json> [--write OUT]
"""
import hashlib
import json
import sys
from pathlib import Path

src, pairs_path = sys.argv[1], sys.argv[2]
with open(src, encoding="utf-8", newline="") as f:  # keep line endings exactly as stored
    text = f.read()
print("source sha256", hashlib.sha256(text.encode("utf-8")).hexdigest()[:12])
pairs = json.loads(Path(pairs_path).read_text(encoding="utf-8"))
bad = 0
for p in sorted(pairs, key=lambda p: (p.get("line", 0), p["id"])):
    want = p.get("expect", 1)
    n = text.count(p["old"])
    if n != want:
        bad += 1
        print(f"FAIL {p['id']}: old occurs {n}x (expected {want}) | {p['old'][:100]}")
        continue
    text = text.replace(p["old"], p["new"])
print(f"{len(pairs) - bad} applied, {bad} failed")
if "--write" in sys.argv:
    out = sys.argv[sys.argv.index("--write") + 1]
    with open(out, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    print("wrote", out, "sha256", hashlib.sha256(text.encode("utf-8")).hexdigest()[:12])
