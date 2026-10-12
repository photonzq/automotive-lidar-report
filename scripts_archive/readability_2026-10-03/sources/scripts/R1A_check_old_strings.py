"""R1_partA_E2-E5: check that every `old` block in a findings file occurs exactly once in the report.

Usage (Anaconda interpreter):
  python R1A_check_old_strings.py <report.md> <findings.md>

Format expected in the findings file: a line containing "`old`:" followed by a fenced block
(``` ... ```), possibly indented as part of a list; the block's own indentation (that of its
opening fence) is removed before matching, so leading spaces of the report line are kept.
Also flags any `new` block that contains a versioning word listed in the spec.
"""
import re
import sys

report = open(sys.argv[1], encoding="utf-8").read()
lines = open(sys.argv[2], encoding="utf-8").read().split("\n")

VERSIONING = re.compile(r"\b(corrected|updated|revised|newly|added)\b", re.I)


def blocks(tag):
    out = []
    i = 0
    while i < len(lines):
        if f"`{tag}`:" in lines[i]:
            j = i + 1
            while j < len(lines) and not lines[j].lstrip().startswith("```"):
                j += 1
            if j >= len(lines):
                break
            indent = len(lines[j]) - len(lines[j].lstrip())
            k = j + 1
            body = []
            while k < len(lines) and not lines[k].strip().startswith("```"):
                body.append(lines[k][indent:] if lines[k][:indent].strip() == "" else lines[k])
                k += 1
            out.append((i + 1, "\n".join(body)))
            i = k + 1
        else:
            i += 1
    return out


bad = 0
for ln, text in blocks("old"):
    n = report.count(text)
    status = "OK" if n == 1 else "PROBLEM"
    if n != 1:
        bad += 1
    print(f"{status}: findings line {ln}: occurs {n}x: {text[:90]!r}")
for ln, text in blocks("new"):
    m = VERSIONING.findall(text)
    if m:
        print(f"WORD CHECK: findings line {ln}: versioning words {m}")
print("old blocks with a count other than 1:", bad)
