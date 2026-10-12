"""Apply a JSON list of {"id", "old", "new"} pairs to the report, hash-guarded (5 Oct 2026).

Used for partB_definitive_edits.json after the separate pass that was to apply them closed first;
the author chose to apply the pairs directly. Every "old" must occur exactly once; the report hash is checked
before reading and again just before writing, so a concurrent change aborts the write.

Usage:
    python apply_json_pairs.py --report <report.md> --pairs <pairs.json> --expect <sha256 prefix>
                               --backup <copy of the report before writing> [--dry]
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--report", required=True)
ap.add_argument("--pairs", required=True)
ap.add_argument("--expect", required=True)
ap.add_argument("--backup", required=True)
ap.add_argument("--dry", action="store_true")
args = ap.parse_args()

RP = Path(args.report)
raw = RP.read_bytes()
h0 = hashlib.sha256(raw).hexdigest()
if not h0.startswith(args.expect):
    sys.exit(f"ABORT: report sha {h0[:12]} does not match the expected {args.expect}")
text = raw.decode("utf-8")
pairs = json.loads(Path(args.pairs).read_text(encoding="utf-8"))

for p in pairs:
    n = text.count(p["old"])
    if n != 1:
        sys.exit(f"ABORT: {p['id']}: old text occurs {n} times")
    text = text.replace(p["old"], p["new"], 1)

out = text.encode("utf-8")
h1 = hashlib.sha256(out).hexdigest()
print(f"{len(pairs)} pairs applied in memory: {h0[:12]} -> {h1[:12]} ({len(raw)} -> {len(out)} bytes)")
if args.dry:
    sys.exit(0)
Path(args.backup).write_bytes(raw)
if hashlib.sha256(RP.read_bytes()).hexdigest() != h0:
    sys.exit("ABORT: report changed during processing; nothing written")
RP.write_bytes(out)
print("written; backup of the previous version at", args.backup)
