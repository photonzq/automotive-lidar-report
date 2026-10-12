"""Structural checks of an edited report copy against the original (read-only).

  - equation tags: same count, sequential; equation references not dangling;
  - section references (§X…) all point to a heading that exists;
  - math delimiters: '$' count parity per changed line (escaped \\$ ignored);
  - changed lines: no doubled spaces, no space before punctuation, no empty bold;
  - headings: lists the headings that changed.

Usage: python validate_report.py <original.md> <edited.md>
"""
import re
import sys
from pathlib import Path

orig = Path(sys.argv[1]).read_text(encoding="utf-8")
new = Path(sys.argv[2]).read_text(encoding="utf-8")


def tags(t):
    return [int(x) for x in re.findall(r"\\tag\{(\d+)\}", t)]


to, tn = tags(orig), tags(new)
print("tags:", len(to), "->", len(tn), "| sequential:", tn == list(range(1, len(tn) + 1)))
REF = re.compile(r"\bEqs?\.\s*\(\d+\)(?:\s*(?:,|and|–|-|to|or)\s*\(\d+\))*")
refs = [int(x) for m in REF.finditer(new) for x in re.findall(r"\((\d+)\)", m.group(0))]
print("equation refs:", len(refs), "| dangling:", sorted({r for r in refs if r < 1 or r > len(tn)}))

heads = re.findall(r"^#{1,6} +(.*)$", new, re.M)
ids = set()
for h in heads:
    m = re.match(r"([A-G][0-9]+[a-z]?(?:\.[0-9]+[a-z]?)*)\.?\s", h)
    if m:
        ids.add(m.group(1))
sec_refs = set(re.findall(r"§([A-G][0-9]+[a-z]?(?:\.[0-9]+[a-z]?)*)", new))
missing = sorted(r for r in sec_refs if r not in ids and r.rstrip(".") not in ids)
print("section refs:", len(sec_refs), "| without a heading:", missing[:30])

ol, nl = orig.split("\n"), new.split("\n")
import difflib
changed = [l for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, ol, nl, autojunk=False).get_opcodes()
           if tag != "equal" for l in nl[j1:j2]]
print("changed lines:", len(changed))
bad = []
for l in changed:
    s = l.replace("\\$", "")
    if s.count("$") % 2:
        bad.append(("odd $", l[:120]))
    if re.search(r"\S  +\S", l) and not l.lstrip().startswith("|"):
        bad.append(("double space", l[:120]))
    if re.search(r" [,.;:)](?!\d)", l) and "$" not in l:
        bad.append(("space before punctuation", l[:120]))
    if "****" in l:
        bad.append(("empty bold", l[:120]))
for k, v in bad:
    print(f"  {k}: {v}")
ho = re.findall(r"^#{1,6} +.*$", orig, re.M)
hn = re.findall(r"^#{1,6} +.*$", new, re.M)
print("headings changed:")
for a, b in zip(ho, hn):
    if a != b:
        print("  -", a, "\n  +", b)
