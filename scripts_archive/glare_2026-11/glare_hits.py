"""Read-only: print every hit of the given patterns in a Markdown report with its line number, the nearest heading
above it and a context window. Usage: glare_hits.py <report.md> <width> <pattern> [<pattern> ...]"""
import re
import sys

path, width, pats = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
lines = open(path, encoding="utf-8").read().split("\n")
heads, cur = [], ""
for ln in lines:
    if re.match(r"^#{1,4} ", ln):
        cur = ln.lstrip("#").strip()
    heads.append(cur)
rx = re.compile("|".join(f"(?:{p})" for p in pats), re.I)
seen = 0
for i, ln in enumerate(lines):
    for m in rx.finditer(ln):
        a, b = max(0, m.start() - width), min(len(ln), m.end() + width)
        print(f"L{i + 1} [{heads[i][:60]}] ...{ln[a:b]}...")
        seen += 1
print("hits:", seen)
