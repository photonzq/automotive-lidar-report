"""Round 2, agent R2F_C9: checks on edits/round2/R2F_C9.json beyond validate_edits.py (writes only to a temp folder).

- applies every edit to an in-memory copy of the live report and confirms the \\tag{} numbers stay sequential;
- flags versioning words, an odd number of unescaped $ and '\\rm' not directly after '{';
- converts sections C9-C9a before and after the edits with pandoc to MathML, as the build does, and reports
  pandoc warnings and <merror> elements.
Usage: python R2F_C9_check_edits.py
"""
import json
import re
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PANDOC = r"pandoc"
rep = (ROOT / "automotive_perception_report_2026-09-27.md").read_text(encoding="utf-8")
d = json.loads((HERE.parents[1] / "edits" / "round2" / "R2F_C9.json").read_text(encoding="utf-8"))

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
    if "@" in e["new"]:
        print("@ in new text", e["id"])

tmp = Path(tempfile.mkdtemp(prefix="r2f_"))
for name, txt in (("before", rep), ("after", new)):
    sec = txt[txt.index("## C9. Lidar-to-lidar"):txt.index("## C10. Can optical")]
    sec = re.sub(r"\{\\rm\s*((?:[^{}]|\{[^{}]*\})*?)\}", r"{\\mathrm{\1}}", sec)
    sec = re.sub(r"\\tag\{(\d+)\}", lambda m: r"\qquad\text{EQMARK" + m.group(1) + "}", sec)
    md, html = tmp / f"c9_{name}.md", tmp / f"c9_{name}.html"
    md.write_text(sec, encoding="utf-8")
    r = subprocess.run([PANDOC, str(md), "-f", "markdown-subscript-superscript-implicit_figures-raw_tex+lists_without_preceding_blankline",
                        "-t", "html5", "--mathml", "-o", str(html)], capture_output=True, text=True, encoding="utf-8")
    warn = [l for l in r.stderr.splitlines() if "WARNING" in l]
    h = html.read_text(encoding="utf-8")
    print(name, "pandoc rc", r.returncode, "warnings", len(warn), "merror", h.count("<merror"), "math", h.count("<math"),
          "EQMARK128", h.count("EQMARK128"))
    for l in warn[:10]:
        print("  ", l)
print("edits", len(d["edits"]), "skipped", len(d["skipped"]))
