"""Parse check of the new section C5b with the build's own math preprocessing and pandoc options (no PDF).

Usage: c5b_parse_check.py <report folder>
Prints pandoc's warnings, and counts the tables, math elements and MathML errors in the section's HTML.
"""
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

folder = Path(sys.argv[1])
sys.path.insert(0, str(folder / "build"))
import eqlabels  # noqa: E402

text = (folder / "automotive_perception_report_2026-09-27.md").read_text(encoding="utf-8")
src = re.sub(r"\{\\rm\s*((?:[^{}]|\{[^{}]*\})*?)\}", r"{\\mathrm{\1}}", text)
assert "{\\rm" not in src
src = eqlabels.resolve(src)
i = src.index("## C5b. Colour lidar")
j = src.index("## C6. How far can SPAD-SoC receivers scale?")
section = src[i:j]
print("equation tags in the section:", re.findall(r"\\tag\{(\d+)\}", section))
tmp = Path(tempfile.mkdtemp())
(tmp / "c5b.md").write_text(section, encoding="utf-8")
cmd = [os.environ.get("PANDOC", "pandoc"), str(tmp / "c5b.md"),
       "-f", "markdown-subscript-superscript-implicit_figures-raw_tex+lists_without_preceding_blankline+autolink_bare_uris",
       "-t", "html5", "--mathml", "--columns=100000", "-o", str(tmp / "c5b.html")]
r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
print("pandoc rc", r.returncode, "warnings:", r.stderr.count("[WARNING]"))
print(r.stderr[:1500])
html = (tmp / "c5b.html").read_text(encoding="utf-8")
print("tables:", html.count("<table"), "math:", html.count("<math"), "merror:", html.count("merror"),
      "list items:", html.count("<li>"), "images:", html.count("<img"))
