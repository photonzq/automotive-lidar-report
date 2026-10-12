"""Check that equation references which name a section point to an equation that is in that section.

After moves and renumbering, a phrase such as "Eq. (33) of §C10.3b" can survive with the right number but the wrong
section. Each tag is located under its "## X." and "### X..." headings; references of the forms "Eq. (N) of §X",
"Eq. (N) (§X", "§X, Eq. (N)", "§X (Eq. (N))" and "§X's Eq. (N)" are listed when the section code X matches neither
heading of tag N (a code matches if it equals the heading's code or extends it, e.g. A6.1 under A6, C0 for any
"subsection" of §C0).
Usage: python check_eq_sections.py [report.md]
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
    r"<report folder>\automotive_perception_report_2026-09-27.md")
lines = path.read_text(encoding="utf-8").split("\n")
CODE = re.compile(r"^#{2,3} ([A-G]\d+[a-z]?(?:\.\d+[a-z]?)?)[. ]")
where = {}
h2 = h3 = None
for i, l in enumerate(lines):
    m = CODE.match(l)
    if m:
        if l.startswith("## "):
            h2, h3 = m.group(1), None
        else:
            h3 = m.group(1)
    for t in re.findall(r"\\tag\{(\d+)\}", l):
        where[int(t)] = (h2, h3, i + 1)

PATS = [re.compile(r"Eq\. \((\d+)\) of §([A-G]\d+[a-z]?(?:\.\d+[a-z]?)?)"),
        re.compile(r"Eq\. \((\d+)\) \(§([A-G]\d+[a-z]?(?:\.\d+[a-z]?)?)"),
        re.compile(r"§([A-G]\d+[a-z]?(?:\.\d+[a-z]?)?)(?:,| subsection [\d.()a-z]+,) Eq\. \((\d+)\)"),
        re.compile(r"§([A-G]\d+[a-z]?(?:\.\d+[a-z]?)?) \(Eq\. \((\d+)\)\)"),
        re.compile(r"§([A-G]\d+[a-z]?(?:\.\d+[a-z]?)?)'s Eq\. \((\d+)\)")]


def ok(code, h2, h3):
    for h in (h2, h3):
        if h and (code == h or code.startswith(h) or h.startswith(code)):
            return True
    return False


bad = 0
for i, l in enumerate(lines):
    for k, p in enumerate(PATS):
        for m in p.finditer(l):
            n, code = (m.group(1), m.group(2)) if k < 2 else (m.group(2), m.group(1))
            n = int(n)
            if n not in where:
                print(f"L{i+1}: Eq. ({n}) has no tag: {m.group(0)}")
                bad += 1
                continue
            h2, h3, at = where[n]
            if not ok(code, h2, h3):
                bad += 1
                print(f"L{i+1}: '{m.group(0)}' but Eq. ({n}) is in {h2}/{h3} (L{at}) …{l[max(0, m.start()-60):m.end()+30]}…")
print(bad, "mismatch(es)")
