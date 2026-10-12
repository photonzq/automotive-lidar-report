"""Apply an edit list to a report copy in memory and print the SHA-256 prefix of the result (no file is written).

Used to confirm that a regenerated archive list reproduces the report sha its merge produced.
Usage: python round4_check_list_reproduces.py <copy.md> <edits.json> [<expected sha prefix>]
"""
import hashlib
import json
import sys
from pathlib import Path

t = Path(sys.argv[1]).read_text(encoding="utf-8")
data = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
spans = []
for e in data["edits"]:
    assert t.count(e["old"]) == 1, e["id"]
    a = t.find(e["old"])
    spans.append((a, a + len(e["old"]), e["new"]))
for a, b, new in sorted(spans, reverse=True):
    t = t[:a] + new + t[b:]
h = hashlib.sha256(t.encode("utf-8")).hexdigest()[:12]
exp = sys.argv[3] if len(sys.argv) > 3 else None
print("result sha", h, "" if exp is None else ("OK" if h == exp else f"MISMATCH (expected {exp})"))
