"""Validate an edit list (JSON) against the live report without writing anything.

Checks, for every edit: its "old" text occurs exactly once in the current report; edits do not overlap each other;
the unescaped-$ parity of "new" matches "old"; no versioning words are introduced; no \\rm directly after a comma or
letter inside a subscript (pandoc texmath rejects it, e.g. write P_{FA,{\\rm pt}}).
Usage: python validate_edits.py edits/<label>.json [more.json ...]
"""
import json
import re
import sys
from pathlib import Path

REPORT = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
DOLLAR = re.compile(r"(?<!\\)\$")
BAD_RM = re.compile(r"_\{[^{}]*[,A-Za-z0-9]\\rm")
VERSIONING = ("corrected", "updated", "revised", " added ", " now ", " newly ")

text = REPORT.read_text(encoding="utf-8")
spans, problems, n_edits = [], [], 0
for path in sys.argv[1:]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    for e in (data if isinstance(data, list) else data.get("edits", [])):
        n_edits += 1
        eid, old, new = e.get("id", "?"), e.get("old", ""), e.get("new", "")
        if not old or old == new:
            problems.append(f"{path}:{eid}: empty or unchanged edit")
            continue
        k = text.count(old)
        if k != 1:
            problems.append(f"{path}:{eid}: 'old' occurs {k} times")
            continue
        start = text.find(old)
        spans.append((start, start + len(old), f"{path}:{eid}"))
        if len(DOLLAR.findall(new)) % 2 != len(DOLLAR.findall(old)) % 2:
            problems.append(f"{path}:{eid}: unbalanced $ in 'new'")
        low_new, low_old = f" {new.lower()} ", f" {old.lower()} "
        for w in VERSIONING:
            if w in low_new and w not in low_old:
                problems.append(f"{path}:{eid}: versioning word {w.strip()!r} introduced")
        if BAD_RM.search(new) and not BAD_RM.search(old):
            problems.append(f"{path}:{eid}: \\rm not directly after '{{' in a subscript (texmath)")
spans.sort()
for (a0, a1, aid), (b0, b1, bid) in zip(spans, spans[1:]):
    if b0 < a1:
        problems.append(f"overlap: {aid} and {bid}")
print(f"{n_edits} edits checked against the live report ({len(text):,} chars)")
for p in problems:
    print("PROBLEM", p)
print("OK" if not problems else f"{len(problems)} problem(s)")
sys.exit(1 if problems else 0)
