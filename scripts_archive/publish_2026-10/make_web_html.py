"""Turn the print HTML that build/build_pdf.py keeps (KEEP_HTML=1) into index.html for GitHub Pages (10 Oct 2026).

- Figures: the print HTML embeds every PNG as a data URI; each is matched by content to its file in
  automotive_perception_report_figures/ and replaced by a relative link, so the page loads its images separately.
- Screen layout: a screen-only stylesheet (centred column, larger type, scrollable wide tables) is added; the print
  styles are left as they are, so printing the page still follows the PDF layout.
- Screen headings: sized relative to the screen type. The print sizes are in points and were set for 9.5 pt text,
  so on screen the subsection headings came out no larger than the text.
- A floating "Contents" link returns to the table of contents; it appears once the reader has scrolled past the
  contents and is hidden when printing.
- A link to the PDF version is placed under the disclaimer on the title block.

Usage (from the report folder, after `KEEP_HTML=1 python build/build_pdf.py`):
    python make_web_html.py <report folder> [--remove-print-html]
"""
import base64
import hashlib
import re
import sys
from pathlib import Path

REPORT = Path(sys.argv[1])
SRC = REPORT / "automotive_perception_report_2026-09-27.html"
OUT = REPORT / "index.html"
FIGS = REPORT / "automotive_perception_report_figures"
PDF_NAME = "automotive_perception_report_2026-09-27.pdf"

SCREEN_CSS = """
<style>
@media screen {
  html { font-size: 11pt; }
  body { max-width: 64rem; margin: 0 auto; padding: 1.5rem 1.25rem 4rem; }
  h1.doc-title { margin-top: 1.5rem; font-size: 2.6rem; }
  h2.doc-subtitle { margin-bottom: 1.2rem; font-size: 1.4rem; }
  h1 { font-size: 2rem; margin-top: 2.4em; }
  h2 { font-size: 1.55rem; margin-top: 1.8em; }
  h3 { font-size: 1.3rem; margin-top: 1.5em; }
  h4 { font-size: 1.12rem; margin-top: 1.2em; }
  table { font-size: 9pt; }
  table.wide { font-size: 8.4pt; }
  .table-scroll { overflow-x: auto; }
  nav#TOC { font-size: 10pt; }
  nav#TOC h1 { font-size: 1.8rem; }
  p.pdf-link { margin: 0.8em 0 1.6em; }
  a.to-contents { position: fixed; right: 1.2rem; bottom: 1.2rem; z-index: 10; padding: 0.4em 0.9em;
    border-radius: 1.2em; background: #1d2f55; color: #fff; font-size: 0.95rem; opacity: 0.85;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3); }
  a.to-contents:hover, a.to-contents:focus { opacity: 1; }
}
@media print {
  a.to-contents { display: none; }
}
</style>
"""

BACK_LINK = """
<a class="to-contents" href="#TOC" title="Back to the table of contents">&#8593; Contents</a>
<script>
(function () {
  var link = document.querySelector("a.to-contents"), toc = document.getElementById("TOC");
  if (!link || !toc) return;
  function update() { link.style.visibility = toc.getBoundingClientRect().bottom < 0 ? "visible" : "hidden"; }
  window.addEventListener("scroll", update, { passive: true });
  update();
})();
</script>
"""

html = SRC.read_text(encoding="utf-8")
by_hash = {hashlib.sha256(p.read_bytes()).hexdigest(): p.name for p in FIGS.glob("*.png")}
unmatched = []


def swap(m):
    data = base64.b64decode(m.group(2))
    name = by_hash.get(hashlib.sha256(data).hexdigest())
    if name is None:
        unmatched.append(len(data))
        return m.group(0)
    return f'src="{FIGS.name}/{name}"'


html, n_img = re.subn(r'src="data:(image/png);base64,([^"]+)"', swap, html)
assert not unmatched, f"{len(unmatched)} embedded images match no figure file"
html = html.replace("</head>", SCREEN_CSS + "</head>", 1)
html = re.sub(r"(<table\b[^>]*>.*?</table>)", r'<div class="table-scroll">\1</div>', html, flags=re.S)
m = re.search(r'<div class="disclaimer">.*?</div>', html, re.S)
assert m, "no disclaimer block found"
link = f'\n<p class="pdf-link"><a href="{PDF_NAME}">PDF version</a> (the figure scripts are attached inside the PDF)</p>'
html = html[:m.end()] + link + html[m.end():]
assert 'id="TOC"' in html, "no table of contents to link back to"
assert html.count("</body>") == 1
html = html.replace("</body>", BACK_LINK + "</body>", 1)
assert "data:image" not in html
OUT.write_text(html, encoding="utf-8", newline="\n")
print(f"{n_img} figures linked; index.html {OUT.stat().st_size / 1e6:.1f} MB")
if "--remove-print-html" in sys.argv:
    SRC.unlink()
    print("removed", SRC.name)
