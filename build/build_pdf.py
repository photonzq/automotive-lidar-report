"""Build the PDF of the automotive perception report.

Pipeline: Markdown -> HTML with MathML (pandoc) -> PDF (headless Chrome) -> post-processing (PyMuPDF).

- Equation numbers: display equations carry \\tag{N} in the Markdown. pandoc's MathML writer drops
  \\tag, so it is swapped for a marker before pandoc and turned into a right-aligned "(N)" with an
  anchor (#eq-N) afterwards.
- Cross-references: "Eq. (N)" and section references such as "§C10.3a", "§C0 subsection 10" or
  "§C0 subsection 10.3" become internal links.
- Source links: bare URLs in the Markdown become links (pandoc's autolink_bare_uris), so the sources can be
  opened from the PDF and the web page.
- Figure code in the PDF: the figure scripts in figures/ (and lidar_equity_prices_weekly.csv, the
  input data of lidar_equity_hype_cycle.py) are embedded as PDF attachments, and a paperclip in the
  left margin beside each figure holds the script that draws it.

- Title page: a fenced div `::: {.disclaimer}` after the subtitle is placed between the subtitle and the
  contents, styled by EXTRA_CSS.

Layout: this file lives in <report>/build; the report is <report>/automotive_perception_report_2026-09-27.md.
Environment settings: PANDOC and CHROME name the two programs (default: `pandoc` and `chrome` on the PATH);
REPORT_MD and REPORT_PDF override the input and output (for tests); KEEP_HTML=1 keeps the print HTML next to the PDF.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString

HERE = Path(__file__).resolve().parent
REPORT_DIR = HERE.parent
FIG_OUT = REPORT_DIR / "automotive_perception_report_figures"  # figure outputs (PNG, PDF, tables)
FIG_SRC = HERE / "figures"  # figure scripts and their input data
MD = Path(os.environ.get("REPORT_MD", str(REPORT_DIR / "automotive_perception_report_2026-09-27.md")))
OUT_PDF = Path(os.environ.get("REPORT_PDF", str(REPORT_DIR / "automotive_perception_report_2026-09-27.pdf")))
PANDOC = os.environ.get("PANDOC", "pandoc")  # pandoc executable; on the PATH by default
CHROME = os.environ.get("CHROME", "chrome")  # Chrome or Chromium executable; on the PATH by default
TITLE = "Automotive Night Vision, Lidar and the Sensor Debate"
EQ_MARK = "EQNOMARK"
EXTRA_CSS = """
.eqn { display: flex; align-items: center; width: 100%; margin: 0.35em 0; }
.eqn-body { flex: 1 1 auto; text-align: center; }
.eqn-no { flex: 0 0 3.4em; text-align: right; color: #272727; }
a.xref { color: #1a4f9c; text-decoration: none; }
.disclaimer { margin: 1.4em 0 0.6em; padding: 0.6em 0.9em; border-left: 3px solid #8a94a6; background: #f4f6f9;
  font-size: 0.92em; }
.disclaimer p { margin: 0; }
"""
# Figures whose script name is not a prefix of the figure's file name
SCRIPT_FOR = {
    "link_budget_loss_vs_range": "link_budget_scaling.py",
    "link_budget_detection_statistics": "link_budget_scaling.py",
    "link_budget_range_scaling": "link_budget_scaling.py",
    "link_budget_margin_weather": "link_budget_scaling.py",
}
T0 = time.time()


def log(*args):
    print(f"[{time.time() - T0:6.0f} s]", *args, flush=True)


def script_for(png: str):
    stem = Path(png).stem
    if stem in SCRIPT_FOR:
        return FIG_SRC / SCRIPT_FOR[stem]
    cands = sorted((p for p in FIG_SRC.glob("*.py") if stem.startswith(p.stem)), key=lambda p: len(p.stem))
    return cands[-1] if cands else None


WORK = Path(tempfile.mkdtemp(prefix="rpdf-"))  # short path: Chrome cannot write very long paths
md_copy = WORK / "report.md"
html_raw = WORK / "report_raw.html"
html_final = WORK / "report_print.html"
pdf_tmp = WORK / "report_print.pdf"

src_md = MD.read_text(encoding="utf-8")
figure_links = re.findall(r"!\[[^\]]*\]\((automotive_perception_report_figures/[^)\s]+\.png)\)", src_md)
src = src_md
# pandoc's TeX-to-MathML converter does not accept the old {\rm ...} font switch
src = re.sub(r"\{\\rm\s*((?:[^{}]|\{[^{}]*\})*?)\}", r"{\\mathrm{\1}}", src)  # one level of nested braces, e.g. {\rm s^{-1}}
assert "{\\rm" not in src, "unconverted {\\rm ...} left"
# equation numbers: \tag{N} -> a marker that survives pandoc's MathML writer
src = re.sub(r"\\tag\{(\d+)\}", lambda m: r"\qquad\text{" + EQ_MARK + m.group(1) + "}", src)
md_copy.write_text(src, encoding="utf-8")

cmd = [
    PANDOC, str(md_copy),
    "-f", "markdown-subscript-superscript-implicit_figures-raw_tex+lists_without_preceding_blankline+autolink_bare_uris",
    "-t", "html5", "--standalone", "--mathml",
    "--toc", "--toc-depth=2", "--columns=100000",
    "--embed-resources", f"--resource-path={REPORT_DIR}",
    f"--css={HERE / 'report.css'}",
    "--metadata", f"pagetitle={TITLE}",
    "--metadata", "lang=en",
    "-o", str(html_raw),
]
r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", cwd=str(REPORT_DIR))
log("pandoc rc", r.returncode, "warnings:", r.stderr.count("[WARNING]"))
print(r.stderr[:2000])
if r.returncode != 0:
    sys.exit(1)

soup = BeautifulSoup(html_raw.read_text(encoding="utf-8"), "html.parser")
body = soup.body
log("HTML parsed")
first_h1 = body.find("h1")
first_h1["class"] = first_h1.get("class", []) + ["doc-title"]
sub = first_h1.find_next("h2")
sub["class"] = sub.get("class", []) + ["doc-subtitle"]

nav = soup.find("nav", id="TOC")
if nav is not None:
    nav.extract()
    top_ul = nav.find("ul")
    first_li = top_ul.find("li", recursive=False) if top_ul else None
    if first_li is not None and TITLE[:20] in first_li.get_text():
        inner = first_li.find("ul")
        if inner is not None:
            for li in list(inner.find_all("li", recursive=False)):
                if li.get_text().strip().startswith("Technology routes"):
                    continue
                first_li.insert_before(li.extract())
        first_li.decompose()
    head = soup.new_tag("h1")
    head.string = "Contents"
    nav.insert(0, head)
    sub.insert_after(nav)
disc = body.find("div", class_="disclaimer")
if disc is not None:  # title page: title, subtitle, disclaimer, then the contents
    sub.insert_after(disc.extract())

for a in body.find_all("a"):
    if a.get_text().strip().startswith(("http://", "https://", "www.")):
        a["class"] = a.get("class", []) + ["url"]

for t in body.find_all("table"):
    ncols = max((len(tr.find_all(["td", "th"], recursive=False)) for tr in t.find_all("tr")), default=0)
    if ncols >= 7:
        t["class"] = t.get("class", []) + ["wide"]

# ---- equation numbers: marker -> right-aligned "(N)" with anchor eq-N
n_eq = 0
for mt in list(body.find_all("mtext")):
    m = re.fullmatch(EQ_MARK + r"(\d+)", mt.get_text().strip())
    if not m:
        continue
    num = m.group(1)
    math = mt.find_parent("math")
    prev = mt.find_previous_sibling()
    if prev is not None and prev.name == "mspace":
        prev.decompose()
    mt.decompose()
    ann = math.find("annotation")
    if ann is not None:
        ann.string = re.sub(r"\\qquad\\text\{" + EQ_MARK + r"\d+\}", "", ann.get_text()).rstrip()
    wrap = soup.new_tag("span", attrs={"class": "eqn", "id": f"eq-{num}"})
    inner = soup.new_tag("span", attrs={"class": "eqn-body"})
    no = soup.new_tag("span", attrs={"class": "eqn-no"})
    no.string = f"({num})"
    math.replace_with(wrap)
    inner.append(math)
    wrap.append(inner)
    wrap.append(no)
    n_eq += 1
left = [mt for mt in body.find_all("mtext") if EQ_MARK in mt.get_text()]
assert not left, f"{len(left)} equation markers left in the HTML"
log("numbered equations", n_eq)

# ---- section anchors from headings
anchors, cur = {}, None
for h in body.find_all(["h1", "h2", "h3", "h4"]):
    hid = h.get("id")
    if not hid:
        continue
    t = h.get_text(" ", strip=True)
    if h.name in ("h1", "h2"):
        m = re.match(r"^([A-G]\d+[a-z]?|\d+)\.\s", t)
        if m:
            anchors.setdefault(m.group(1), hid)
            cur = m.group(1)
        m = re.match(r"^Appendix (\d+)", t)
        if m:
            anchors.setdefault(f"Appendix {m.group(1)}", hid)
        m = re.match(r"^Part ([A-G])\b", t)
        if m:
            anchors.setdefault(f"Part {m.group(1)}", hid)
    else:
        m = re.match(r"^([A-G]\d+[a-z]?\.\d+[a-z]?)\b", t) or re.match(r"^([A-G]\d+[a-z]?)\.\s", t)
        if m:
            anchors.setdefault(m.group(1), hid)
        m = re.match(r"^(\d+)\.\s", t) or re.match(r"^(\d+\.\d+)\s", t)  # "10. Link budget" or "10.2 How much light"
        if m and cur:
            anchors.setdefault(f"{cur} subsection {m.group(1)}", hid)

REF_RE = re.compile(
    r"(?P<sec>§\s?(?P<code>[A-G]\d+[a-z]?(?:\.\d+[a-z]?)?|0)(?:\s+subsections?\s+(?P<sub>\d+(?:\.\d+)?))?)"
    r"|(?P<eqs>\bEqs?\.\s*\(\d+\)(?:\s*(?:,|and|–|-|to|or)\s*\(\d+\))*)"
)
SKIP = {"a", "math", "code", "pre", "h1", "h2", "h3", "h4", "nav", "script", "style", "annotation", "title"}
n_sec = n_eqref = 0


def target(code, sub_no):
    if sub_no and f"{code} subsection {sub_no}" in anchors:
        return anchors[f"{code} subsection {sub_no}"]
    if code in anchors:
        return anchors[code]
    base = re.match(r"^([A-G]\d+[a-z]?)", code)
    return anchors.get(base.group(1)) if base else None


for s in list(body.find_all(string=True)):
    if not isinstance(s, NavigableString) or not ("§" in s or "Eq" in s):
        continue
    if any(p.name in SKIP for p in s.parents if p is not None and p.name):
        continue
    text = str(s)
    pieces, pos = [], 0
    for m in REF_RE.finditer(text):
        if m.group("sec"):
            tid = target(m.group("code"), m.group("sub"))
            if not tid:
                continue
            pieces.append(text[pos:m.start()])
            a = soup.new_tag("a", href=f"#{tid}", attrs={"class": "xref"})
            a.string = m.group(0)
            pieces.append(a)
            n_sec += 1
        else:
            pieces.append(text[pos:m.start()])
            phrase, ppos = m.group(0), 0
            for mm in re.finditer(r"\((\d+)\)", phrase):
                pieces.append(phrase[ppos:mm.start()])
                a = soup.new_tag("a", href=f"#eq-{mm.group(1)}", attrs={"class": "xref"})
                a.string = mm.group(0)
                pieces.append(a)
                ppos = mm.end()
                n_eqref += 1
            pieces.append(phrase[ppos:])
        pos = m.end()
    if not pieces:
        continue
    pieces.append(text[pos:])
    first = True
    for p in pieces:
        node = NavigableString(p) if isinstance(p, str) else p
        if first:
            s.replace_with(node)
            last = node
            first = False
        else:
            last.insert_after(node)
            last = node
log("section links", n_sec, "equation links", n_eqref, "anchors", len(anchors))

style = soup.new_tag("style")
style.string = EXTRA_CSS
soup.head.append(style)

html_final.write_text(str(soup), encoding="utf-8")
log("html bytes", html_final.stat().st_size)

profile = WORK / "profile"
ccmd = [
    CHROME, "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
    "--disable-extensions", f"--user-data-dir={profile}",
    "--no-pdf-header-footer", "--generate-pdf-document-outline",
    "--run-all-compositor-stages-before-draw", "--virtual-time-budget=60000",
    f"--print-to-pdf={pdf_tmp}", html_final.as_uri(),
]
r = subprocess.run(ccmd, capture_output=True, text=True, timeout=1800)
log("chrome rc", r.returncode, (r.stderr or "")[-800:])
if not pdf_tmp.exists():
    sys.exit(2)

import pymupdf  # noqa: E402

doc = pymupdf.open(pdf_tmp)
toc = doc.get_toc(simple=False)
if toc and toc[0][1].replace(" ", "") == TITLE.replace(" ", ""):
    toc[0][1] = TITLE  # Chrome drops the space at the title's line wrap
    doc.set_toc(toc)

# ---- figure code in the PDF: attach the figure scripts and the one input data file they need
drawn_by = {}
for png in figure_links:
    sp = script_for(png)
    if sp is not None:
        drawn_by.setdefault(sp.name, []).append(Path(png).name)
attachments = []
for p in sorted(FIG_SRC.glob("*.py")):
    what = ", ".join(drawn_by.get(p.name, [])) or "the §C4c eye-safety and sunlight tables (no figure)"
    attachments.append((f"build/figures/{p.name}", p, f"Figure script: draws {what}"))
for p in sorted(FIG_SRC.glob("*.csv")):
    attachments.append((f"build/figures/{p.name}", p, "Input data for lidar_equity_hype_cycle.py (keep it in the same folder)"))
for key, path, desc in attachments:
    doc.embfile_add(key, path.read_bytes(), filename=path.name, ufilename=path.name, desc=desc)
log("attached files", doc.embfile_count())

# ---- a paperclip beside each figure, holding the script that draws it
placed = []
for page in doc:
    for info in page.get_image_info():
        rect = pymupdf.Rect(info["bbox"])
        if rect.width >= 100 and rect.height >= 60:
            placed.append((page.number, rect.y0, rect.x0, rect))
placed.sort(key=lambda x: (x[0], x[1], x[2]))
n_clip = 0
if len(placed) == len(figure_links):
    for (pno, _, _, rect), png in zip(placed, figure_links):
        sp = script_for(png)
        if sp is None:
            continue
        page = doc[pno]
        pos = pymupdf.Point(max(4.0, rect.x0 - 24.0), rect.y0 + 2.0)
        annot = page.add_file_annot(pos, sp.read_bytes(), sp.name, ufilename=sp.name,
                                    desc=f"Script that draws {Path(png).name} (build/figures/{sp.name})",
                                    icon="Paperclip")
        annot.set_info(title="Figure script", content=f"build/figures/{sp.name} draws this figure ({Path(png).name}).")
        annot.update()
        n_clip += 1
else:
    log(f"WARNING: {len(placed)} images in the PDF but {len(figure_links)} figure links in the Markdown; paperclips skipped")
log("figure paperclips", n_clip)

doc.set_metadata({
    "title": TITLE,
    "subject": "Technology routes, markets, supply chain, geopolitics and outlook",
    "author": "",
    "keywords": "lidar; thermal night vision; FMCW; SPAD; automotive perception",
    "creator": "",
    "producer": "",
})
doc.save(OUT_PDF, garbage=2, deflate=True)  # garbage=3 (object dedup) takes ~8 min here for the same size
if os.environ.get("KEEP_HTML"):
    shutil.copy2(html_final, OUT_PDF.with_suffix(".html"))
log("pages", doc.page_count, "toc entries", len(doc.get_toc()), "size MB", round(OUT_PDF.stat().st_size / 1e6, 1))
doc.close()
shutil.rmtree(WORK, ignore_errors=True)
