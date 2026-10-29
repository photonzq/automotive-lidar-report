"""Classify the differences between the report and its work copy: lines that differ only in numbers
(renumbered tags and references) versus real text changes, which are printed.

Usage: python diff_classify.py <original.md> <work.md>
"""
import difflib
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
a = Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()
b = Path(sys.argv[2]).read_text(encoding="utf-8").splitlines()
norm = lambda s: re.sub(r"\d+", "#", s)
num_only = 0
for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
    if op == "equal":
        continue
    if op == "replace" and i2 - i1 == j2 - j1 and all(norm(x) == norm(y) for x, y in zip(a[i1:i2], b[j1:j2])):
        num_only += i2 - i1
        # every number change must sit inside "\tag{N}" or an "Eq(s). (N)" reference
        for x, y in zip(a[i1:i2], b[j1:j2]):
            sx = re.sub(r"\\tag\{\d+\}|\bEqs?\.\s*\(\d+\)(?:\s*(?:,|and|–|-|to|or)\s*\(\d+\))*", "@", x)
            sy = re.sub(r"\\tag\{\d+\}|\bEqs?\.\s*\(\d+\)(?:\s*(?:,|and|–|-|to|or)\s*\(\d+\))*", "@", y)
            if sx != sy:
                print("NUMBER CHANGE OUTSIDE A TAG OR REFERENCE at line", i1 + 1, ":", x[:160])
        continue
    print(f"--- {op} original {i1 + 1}-{i2} -> work {j1 + 1}-{j2}")
    for x in a[i1:i2]:
        print("  - " + x[:150])
    for y in b[j1:j2]:
        print("  + " + y[:150])
print("lines changed only in tag/reference numbers:", num_only)
