"""Apply a JSON list of edit pairs to one file, hash-guarded, keeping its line endings.

Each pair is {"id", "old", "new"} with an optional "expect" (number of identical occurrences, all replaced;
default 1). The file's sha256 must start with --expect; every "old" must occur exactly "expect" times at its
turn; the file is copied to --backup first and re-hashed just before writing, so a concurrent change aborts.

Usage: python apply_pairs.py --file F --pairs P.json --expect SHA_PREFIX --backup DIR
"""
import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--file", required=True)
ap.add_argument("--pairs", required=True)
ap.add_argument("--expect", required=True)
ap.add_argument("--backup", required=True)
a = ap.parse_args()

f = Path(a.file)
raw = f.read_bytes()
sha = hashlib.sha256(raw).hexdigest()
if not sha.startswith(a.expect):
    sys.exit(f"hash mismatch: {sha[:12]} (expected {a.expect}); nothing written")
text = raw.decode("utf-8")
pairs = json.loads(Path(a.pairs).read_text(encoding="utf-8"))
for p in sorted(pairs, key=lambda p: (p.get("line", 0), p["id"])):
    want = p.get("expect", 1)
    n = text.count(p["old"])
    if n != want:
        sys.exit(f"{p['id']}: old occurs {n}x (expected {want}); nothing written")
    text = text.replace(p["old"], p["new"])
bk = Path(a.backup)
bk.mkdir(parents=True, exist_ok=True)
shutil.copy2(f, bk / f.name)
if hashlib.sha256(f.read_bytes()).hexdigest() != sha:
    sys.exit("file changed while the edits were prepared; nothing written")
f.write_bytes(text.encode("utf-8"))
print(f"{f.name}: {len(pairs)} pairs applied; sha256 {sha[:12]} -> {hashlib.sha256(text.encode('utf-8')).hexdigest()[:12]}")
