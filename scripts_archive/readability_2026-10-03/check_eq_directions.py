"""List equation references whose "below"/"above" no longer matches where the tagged equation sits.

A reference "Eq. (N) below" is wrong if tag N stands on an earlier line, and "Eq. (N) above" if it stands later;
moving numbered material can flip either.
Usage: python check_eq_directions.py [report.md]
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
    r"<report folder>\automotive_perception_report_2026-09-27.md")
lines = path.read_text(encoding="utf-8").split("\n")
tag = {}
for i, l in enumerate(lines):
    for t in re.findall(r"\\tag\{(\d+)\}", l):
        tag[int(t)] = i
REF = re.compile(r"Eqs?\. \((\d+)\)(?:\s*[–-]\s*\((\d+)\))?,? (below|above)")
wrong = 0
for i, l in enumerate(lines):
    for m in REF.finditer(l):
        k, d = int(m.group(1)), m.group(3)
        if k not in tag:
            print(f"L{i+1}: no tag {k}")
            continue
        if (d == "below" and tag[k] < i) or (d == "above" and tag[k] > i):
            wrong += 1
            print(f"L{i+1}: {m.group(0)!r}, tag at L{tag[k]+1}: …{l[max(0, m.start()-90):m.end()+20]}…")
print(len(tag), "tags;", wrong, "reference(s) pointing the wrong way")
