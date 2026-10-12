"""Round 2, agent R2D_C7b: checks on edits/round2/R2D_C7b.json beyond validate_edits.py (writes only to a temp folder).

- applies every edit to an in-memory copy of the live report and confirms the 188 \\tag{} stay sequential;
- flags versioning words, an odd number of unescaped $, '\\rm' not directly after '{' and a bold paragraph newly
  glued to a list item;
- converts section C7b before and after the edits with pandoc to MathML, as build/build_pdf.py does, and reports
  pandoc warnings and <merror> elements.
Usage: python r2d_c7b_check_edits.py
"""
import json
import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PANDOC = r"pandoc"
rep = (ROOT / "automotive_perception_report_2026-09-27.md").read_text(encoding="utf-8")
d = json.loads((ROOT / "scripts_archive/readability_2026-10-03/edits/round2/R2D_C7b.json").read_text(encoding="utf-8"))

new = rep
for e in d["edits"]:
    assert new.count(e["old"]) == 1, e["id"]
    new = new.replace(e["old"], e["new"])
tags = [int(x) for x in re.findall(r"\\tag\{(\d+)\}", new)]
print("tags", len(tags), "sequential", tags == list(range(1, len(tags) + 1)))
for e in d["edits"]:
    lo_new, lo_old = e["new"].lower(), e["old"].lower()
    for w in (" new ", " newly", " now ", "earlier", "previous", "corrected", "updated", "revised", " added", "formerly"):
        if w in lo_new and w not in lo_old:
            print("versioning word", repr(w), e["id"])
    if len(re.findall(r"(?<!\\)\$", e["new"])) % 2:
        print("odd $", e["id"])
    if re.search(r"_\{[^{}]*[,A-Za-z0-9]\\rm", e["new"]):
        print("\\rm not after {", e["id"])


def glued(txt):
    lines = txt.split("\n")
    return {lines[i][:80] for i in range(1, len(lines))
            if lines[i].startswith("**") and re.match(r"^\s*([-*]|\d+\.)\s", lines[i - 1])}


print("bold paragraphs newly glued to a list item:", sorted(glued(new) - glued(rep)))

tmp = Path(tempfile.mkdtemp(prefix="r2d_"))
for name, txt in (("before", rep), ("after", new)):
    sec = txt[txt.index("## C7b. Can FMCW win?"):txt.index("## C8. Chip-size")]
    sec = re.sub(r"\{\\rm\s*((?:[^{}]|\{[^{}]*\})*?)\}", r"{\\mathrm{\1}}", sec)
    sec = re.sub(r"\\tag\{(\d+)\}", lambda m: r"\qquad\text{EQMARK" + m.group(1) + "}", sec)
    md, html = tmp / f"c7b_{name}.md", tmp / f"c7b_{name}.html"
    md.write_text(sec, encoding="utf-8")
    r = subprocess.run([PANDOC, str(md), "-f", "markdown-subscript-superscript-implicit_figures-raw_tex+lists_without_preceding_blankline",
                        "-t", "html5", "--mathml", "-o", str(html)], capture_output=True, text=True, encoding="utf-8")
    warn = [l for l in r.stderr.splitlines() if "WARNING" in l]
    out = html.read_text(encoding="utf-8")
    print(name, "pandoc rc", r.returncode, "warnings", len(warn), "merror", out.count("<merror"),
          "tables", out.count("<table"), "math", out.count("<math"))
    for w in warn[:10]:
        print("   ", w[:160])
print("edits", len(d["edits"]), "skipped", len(d["skipped"]))
