"""Write a scratch copy of the archived renumber_equations.py that works on the given working copy of the report.
Usage: python make_renumber_copy.py <archived tool> <scratch copy out> <working copy of the report>
"""
import sys

src = open(sys.argv[1], encoding="utf-8").read()
old = 'REPORT = Path(r"<report folder>\\automotive_perception_report_2026-09-27.md")'
assert src.count(old) == 1, src.count(old)
open(sys.argv[2], "w", encoding="utf-8").write(src.replace(old, f'REPORT = Path(r"{sys.argv[3]}")'))
print("scratch copy written")
