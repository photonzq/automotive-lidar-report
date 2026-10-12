"""R7: check that every `old` string of a findings file occurs exactly once in the report.

Usage: python R7_check_old_strings.py <findings.md> <report.md>
The findings file holds each `old` string in a fenced block on the lines after a line
containing "`old`". Prints the SHA-256 prefix of the report, then one line per block:
count, item heading and the first 90 characters of the string. Exit status 1 if any
count differs from 1.
"""
import hashlib
import re
import sys

findings, report = sys.argv[1], sys.argv[2]
rep = open(report, encoding="utf-8").read()
print("report sha256:", hashlib.sha256(open(report, "rb").read()).hexdigest()[:12])
lines = open(findings, encoding="utf-8").read().split("\n")
item, bad, n = "?", 0, 0
i = 0
while i < len(lines):
    ln = lines[i]
    if ln.startswith("## "):
        item = ln[3:].strip()
    if re.match(r"^\s*- `old`", ln):
        j = i + 1
        while j < len(lines) and not lines[j].startswith("```"):
            j += 1
        k = j + 1
        while k < len(lines) and not lines[k].startswith("```"):
            k += 1
        s = "\n".join(lines[j + 1:k])
        c = rep.count(s)
        n += 1
        bad += c != 1
        print(f"{c}  {item}  {s[:90]!r}")
        i = k
    i += 1
print(f"{n} old strings checked, {bad} not unique or missing")
sys.exit(1 if bad else 0)
