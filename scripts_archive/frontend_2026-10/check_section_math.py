"""Convert one report section with pandoc, exactly as build/build_pdf.py prepares the math,
and report any formula pandoc cannot convert.

Usage: python check_section_math.py <report.md> "<first heading line>" "<next heading line>" [pandoc]
The section runs from the first heading line up to, not including, the next heading line.
"""
import re
import subprocess
import sys
from pathlib import Path

report, start, stop = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
pandoc = sys.argv[4] if len(sys.argv) > 4 else "pandoc"
lines = report.read_text(encoding="utf-8").splitlines()
i0 = lines.index(start)
i1 = lines.index(stop, i0 + 1)
src = "\n".join(lines[i0:i1]) + "\n"
# same preprocessing as build/build_pdf.py
src = re.sub(r"\{\\rm\s*((?:[^{}]|\{[^{}]*\})*?)\}", r"{\\mathrm{\1}}", src)
assert "{\\rm" not in src, "unconverted {\\rm ...} left"
src = re.sub(r"\\tag\{(\d+)\}", "", src)
res = subprocess.run(
    [pandoc, "-f", "markdown-subscript-superscript-implicit_figures-raw_tex"
     "+lists_without_preceding_blankline+autolink_bare_uris", "-t", "html5", "--mathml"],
    input=src, capture_output=True, text=True, encoding="utf-8")
print(f"lines {i0 + 1}-{i1}: {src.count('$') // 2} inline/display math spans (approx.), "
      f"{res.stdout.count('<math')} converted to MathML")
bad = [l for l in res.stderr.splitlines() if "Could not convert" in l]
print("\n".join(bad) if bad else "no math conversion warnings")
