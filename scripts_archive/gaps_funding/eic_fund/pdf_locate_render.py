"""Locate search terms in a PDF (text layer only) and render pages to PNG.

Usage (run from the eic_fund folder):
    python scripts/pdf_locate_render.py raw/file.pdf --find term1 term2 ...
    python scripts/pdf_locate_render.py raw/file.pdf --render 1 2 5   (1-based)
    python scripts/pdf_locate_render.py raw/file.pdf --render-hits term1 ...
Text extraction is used only to find which page to look at; the page is then
rendered at 160 dpi (override with --dpi N) to png/<pdfstem>_p<N>.png so the
page can be read as an image.
"""
import argparse
from pathlib import Path

import pymupdf

PNG = Path("png")
PNG.mkdir(exist_ok=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--find", nargs="*", default=[])
    ap.add_argument("--render", nargs="*", type=int, default=[])
    ap.add_argument("--render-hits", nargs="*", default=[])
    ap.add_argument("--dpi", type=int, default=160)
    a = ap.parse_args()
    doc = pymupdf.open(a.pdf)
    stem = Path(a.pdf).stem[:60]
    print(f"{a.pdf}: {doc.page_count} pages")
    terms = a.find + a.render_hits
    hits = []
    for i, page in enumerate(doc):
        txt = page.get_text().lower()
        for t in terms:
            if t.lower() in txt:
                hits.append(i + 1)
                j = txt.index(t.lower())
                snippet = txt[max(0, j - 120): j + 200].replace("\n", " | ")
                print(f"p{i + 1} [{t}]: ...{snippet}...")
    pages = set(a.render)
    if a.render_hits:
        pages |= set(hits)
    for p in sorted(pages):
        out = PNG / f"{stem}_p{p}.png"
        doc[p - 1].get_pixmap(dpi=a.dpi).save(out)
        print("rendered", out)


if __name__ == "__main__":
    main()
