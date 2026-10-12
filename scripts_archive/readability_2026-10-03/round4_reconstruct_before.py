"""Reconstruct the report as it was before one applied Round 4 list, to regenerate that list's archived JSON.

Reverse-applies the list's text edits (each "new" must occur once and becomes "old") and removes the Appendix 2
lines the batch added (taken from the findings file), then prints the SHA-256 prefix of the result, which must
match the sha the merge started from. Writes the copy to the given output path; the report is only read.
Usage: python round4_reconstruct_before.py <edits.json> <findings.md> <out.md> <expected sha prefix>
"""
import hashlib
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
REPORT = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
edits_path, findings, out, expect = sys.argv[1:5]
t = REPORT.read_text(encoding="utf-8")
data = json.loads(Path(edits_path).read_text(encoding="utf-8"))
for e in data["edits"]:
    if "-A2-" in e["id"]:
        continue
    assert t.count(e["new"]) == 1, (e["id"], t.count(e["new"]))
    t = t.replace(e["new"], e["old"])
for line in re.findall(r"(?m)^\s*- `(- .+)`\s*$", Path(findings).read_text(encoding="utf-8")):
    k = t.count("\n" + line + "\n")
    if k == 1:
        t = t.replace("\n" + line + "\n", "\n", 1)
Path(out).write_bytes(t.encode("utf-8"))
h = hashlib.sha256(t.encode("utf-8")).hexdigest()[:12]
print("reconstructed sha", h, "OK" if h == expect else f"MISMATCH (expected {expect})")
