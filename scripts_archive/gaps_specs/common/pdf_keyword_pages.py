"""Locate pages of a long PDF (prospectus, annual report, paper) by regular
expression and render the matching pages to PNG for visual reading.

Text extraction (PyMuPDF get_text) is used only to find pages; the rendered
PNGs are what is read, so that tables and figures are seen as printed.
Used on the Hesai Hong Kong prospectus (8 Sep 2025; supplier tables on
printed pp. 302-304), RoboSense's prospectus and annual reports, the XMC
STAR-market prospectus, the InnovizTwo datasheet and conference programmes.

Usage : python pdf_keyword_pages.py <file.pdf> "<regex>" [--render] [--dpi 160]
            [--context 220] [--max-hits 3]
Output: prints page numbers (1-based) with text windows around each hit;
        with --render, writes <stem>_p<page>.png next to the folder given by
        GAPS_SPECS_RAW (default ".").
"""
import argparse
import os
import re

import pymupdf

OUT = os.environ.get("GAPS_SPECS_RAW", ".")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("regex")
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--dpi", type=int, default=160)
    ap.add_argument("--context", type=int, default=220)
    ap.add_argument("--max-hits", type=int, default=3)
    a = ap.parse_args()
    pat = re.compile(a.regex, re.I)
    doc = pymupdf.open(a.pdf)
    stem = os.path.splitext(os.path.basename(a.pdf))[0]
    print("pages:", doc.page_count)
    for i, page in enumerate(doc):
        text = page.get_text()
        hits = list(pat.finditer(text))
        if not hits:
            continue
        print(f"== page {i + 1}: {len(hits)} hit(s)")
        for m in hits[: a.max_hits]:
            s = max(0, m.start() - a.context)
            print("    ", text[s: m.end() + a.context].replace("\n", " "))
        if a.render:
            fn = os.path.join(OUT, f"{stem}_p{i + 1}.png")
            page.get_pixmap(dpi=a.dpi).save(fn)
            print("    rendered", fn)


if __name__ == "__main__":
    main()
