"""Checks the math of edits/round2/R2C_C7-C7a.json the way build/build_pdf.py converts it.

Applies the build's {\\rm ...} -> {\\mathrm{...}} rewrite and its \\tag marker, runs pandoc with the build's
reader and MathML writer on all "old" and all "new" texts, and reports pandoc warnings and <merror> counts.
Writes only to a temporary folder. Run from the report folder:
  python scripts_archive/readability_2026-10-03/round2/scripts/r2c_check_math.py
"""
import json
import re
import subprocess
import tempfile
from pathlib import Path

PANDOC = r"pandoc"
HERE = Path(__file__).resolve().parent
EDITS = HERE.parents[1] / "edits" / "round2" / "R2C_C7-C7a.json"
WORK = Path(tempfile.mkdtemp(prefix="r2c-math-"))
d = json.loads(EDITS.read_text(encoding="utf-8"))


def prep(src):
    src = re.sub(r"\{\\rm\s*((?:[^{}]|\{[^{}]*\})*?)\}", lambda m: "{\\mathrm{" + m.group(1) + "}}", src)
    assert "{\\rm" not in src
    return re.sub(r"\\tag\{(\d+)\}", lambda m: "\\qquad\\text{EQ" + m.group(1) + "}", src)


def run(name, text):
    md, out = WORK / (name + ".md"), WORK / (name + ".html")
    md.write_text(prep(text), encoding="utf-8")
    r = subprocess.run([PANDOC, str(md), "-f", "markdown-subscript-superscript-implicit_figures-raw_tex+lists_without_preceding_blankline",
                        "-t", "html5", "--mathml", "--columns=100000", "-o", str(out)], capture_output=True, text=True, encoding="utf-8")
    html = out.read_text(encoding="utf-8")
    print(name, "rc", r.returncode, "warnings", r.stderr.count("[WARNING]"), "merror", html.count("<merror"), "math", html.count("<math"))
    if r.stderr.strip():
        print(r.stderr[:3000])


run("old", "\n\n".join(e["old"] for e in d["edits"]))
run("new", "\n\n".join(e["new"] for e in d["edits"]))
