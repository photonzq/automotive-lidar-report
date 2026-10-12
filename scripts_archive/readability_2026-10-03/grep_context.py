"""Print every match of one or more regular expressions in the report, with line number and a context window.

Usage: python grep_context.py [-w WIDTH] [--file PATH] PATTERN [PATTERN ...]
WIDTH is the number of characters shown on each side of a match (default 160). Matches are case-sensitive.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
REPORT = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
args = sys.argv[1:]
width = 160
if args[:1] == ["-w"]:
    width, args = int(args[1]), args[2:]
if args[:1] == ["--file"]:
    REPORT, args = Path(args[1]), args[2:]
text = REPORT.read_text(encoding="utf-8")
line_starts = [0] + [m.end() for m in re.finditer("\n", text)]


def line_of(pos):
    lo, hi = 0, len(line_starts) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if line_starts[mid] <= pos:
            lo = mid
        else:
            hi = mid - 1
    return lo + 1


for pat in args:
    hits = list(re.finditer(pat, text))
    print(f"### {pat!r}: {len(hits)} match(es)")
    for m in hits[:40]:
        a, b = max(0, m.start() - width), min(len(text), m.end() + width)
        snippet = text[a:b].replace("\n", " ⏎ ")
        print(f"  L{line_of(m.start())}: …{snippet}…")
    if len(hits) > 40:
        print(f"  ({len(hits) - 40} more not shown)")
