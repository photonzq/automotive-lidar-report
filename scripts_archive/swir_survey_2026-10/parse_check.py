"""Static parse check of a report Markdown file without building a PDF: resolve the equation labels and the {\\rm} switch as
build/build_pdf.py does, run pandoc to HTML with MathML, and print pandoc's warnings and any math pandoc could not convert.
Usage: parse_check.py <report folder> <document.md> <pandoc executable> <scratch folder>"""
import re
import subprocess
import sys
from pathlib import Path

report, doc, pandoc, scratch = Path(sys.argv[1]), sys.argv[2], sys.argv[3], Path(sys.argv[4])
sys.path.insert(0, str(report / "build"))
import eqlabels  # noqa: E402

src = (report / doc).read_text(encoding="utf-8")
src = re.sub(r"\{\\rm\s*((?:[^{}]|\{[^{}]*\})*?)\}", r"{\\mathrm{\1}}", src)
src = eqlabels.resolve(src)
md = scratch / "parse_check.md"
html = scratch / "parse_check.html"
md.write_text(src, encoding="utf-8")
r = subprocess.run([pandoc, str(md), "-f",
                    "markdown-subscript-superscript-implicit_figures-raw_tex+lists_without_preceding_blankline+autolink_bare_uris",
                    "-t", "html5", "--mathml", "-o", str(html)], capture_output=True, text=True, encoding="utf-8")
print("pandoc rc", r.returncode, "warnings", r.stderr.count("[WARNING]"))
print(r.stderr[:3000])
out = html.read_text(encoding="utf-8")
print("unconverted math spans:", len(re.findall(r'class="math', out)))
print("equation tags:", len(re.findall(r"\\tag\{\d+\}", src)))
