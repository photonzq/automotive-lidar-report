"""Collect the 'skipped' items of all Round 1 edit lists into one Markdown file, grouped by kind.

The kinds are model_round2, structural, needs_source, needs_decision, cross_section and already_fixed. The output
is the work list for Rounds 2-4 and for the questions to the author.
Usage: python collect_skipped.py OUT.md
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

EDITS = Path(__file__).resolve().parent / "edits"
groups = defaultdict(list)
for path in sorted(EDITS.glob("*.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        continue
    for s in data.get("skipped", []):
        groups[s.get("kind", "?")].append((path.stem, s))
out = ["# Round 1 skipped items, by kind", ""]
for kind in ("model_round2", "structural", "needs_decision", "needs_source", "cross_section", "already_fixed"):
    items = groups.get(kind, [])
    out += [f"## {kind} ({len(items)})", ""]
    for stem, s in items:
        out.append(f"- **[{stem}] {s.get('finding', '')}** @ {s.get('location', '')}")
        out.append(f"  - {s.get('detail', '')}")
    out.append("")
Path(sys.argv[1]).write_text("\n".join(out), encoding="utf-8")
print({k: len(v) for k, v in groups.items()})
