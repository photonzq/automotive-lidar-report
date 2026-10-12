"""Print, for each literal string, how often it occurs in the report and the full line(s) holding it.

Used to copy exact "old" strings into a hand-written edit list. Long lines are cut to WIDTH characters on each
side of the match.
Usage: python find_literal.py [-w WIDTH] "literal one" "literal two" ...
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
REPORT = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
args = sys.argv[1:]
width = 400
if args[:1] == ["-w"]:
    width, args = int(args[1]), args[2:]
text = REPORT.read_text(encoding="utf-8")
for lit in args:
    k = text.count(lit)
    print(f"### {lit!r}: {k}")
    start = 0
    for _ in range(min(k, 6)):
        i = text.find(lit, start)
        a = text.rfind("\n", 0, i) + 1
        b = text.find("\n", i)
        b = len(text) if b < 0 else b
        lo, hi = max(a, i - width), min(b, i + len(lit) + width)
        line_no = text.count("\n", 0, i) + 1
        print(f"  L{line_no}: {'…' if lo > a else ''}{text[lo:hi]}{'…' if hi < b else ''}")
        start = i + 1
