"""Print selected report lines with their numbers.

Usage: python show_lines.py <report.md> 172 958 2105-2112 ...
"""
import sys
from pathlib import Path

lines = Path(sys.argv[1]).read_text(encoding="utf-8").split("\n")
for arg in sys.argv[2:]:
    if "-" in arg:
        a, b = (int(x) for x in arg.split("-"))
    else:
        a = b = int(arg)
    for n in range(a, b + 1):
        print(f"{n}: {lines[n - 1]}")
    print("-----")
