"""Parse check of the whole report with the build's own math preprocessing and pandoc options (no PDF).

Usage: full_parse_check.py <report folder>
Set PANDOC to the pandoc executable if it is not on the PATH. Prints pandoc's return code and warnings, and counts
the math elements and MathML errors in the resulting HTML.
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
tmp = Path(tempfile.mkdtemp())
(tmp / "report.md").write_text(src, encoding="utf-8")
cmd = [os.environ.get("PANDOC", "pandoc"), str(tmp / "report.md"),
       "-f", "markdown-subscript-superscript-implicit_figures-raw_tex+lists_without_preceding_blankline+autolink_bare_uris",
       "-t", "html5", "--mathml", "--columns=100000", "-o", str(tmp / "report.html")]
r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", cwd=str(folder))
print("pandoc rc", r.returncode, "warnings:", r.stderr.count("[WARNING]"))
print(r.stderr[:1500])
html = (tmp / "report.html").read_text(encoding="utf-8")
print("math:", html.count("<math"), "merror:", html.count("merror"))
