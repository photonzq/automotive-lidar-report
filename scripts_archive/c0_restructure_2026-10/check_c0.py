"""Checks on the new §C0 of a working copy: odd '$' lines, doubled spaces, untagged displays, tag range;
writes the section to new_c0_final.md for reading.
Usage: python check_c0.py <working copy>
"""
import re
import sys

t = open(sys.argv[1], encoding="utf-8").read()
c0 = t[t.index("## C0. Physics of lidar ranging"):t.index("## C1. Taxonomy")]
open("new_c0_final.md", "w", encoding="utf-8").write(c0)
lines = c0.split("\n")
odd = [l[:120] for l in lines if len(re.findall(r"(?<!\\)\$", l)) % 2]
print("odd-$ lines:", len(odd))
for o in odd[:10]:
    print("   ", o)
dbl = [l[:100] for l in lines if "  " in l.strip() and not l.lstrip().startswith("|")]
print("lines with doubled spaces:", len(dbl))
for d in dbl[:5]:
    print("   ", d)
disp = re.findall(r"\$\$(.+?)\$\$", c0, flags=re.S)
tags = re.findall(r"\\tag\{(\d+)\}", c0)
print("display equations:", len(disp), "| untagged:", sum(1 for d in disp if "\\tag{" not in d), "| tags", tags[0], "to", tags[-1])
print("lines:", len(lines), "| bytes:", len(c0.encode("utf-8")))
heads = [l for l in lines if l.startswith("#")]
print("headings:")
for h in heads:
    print("   ", h)
