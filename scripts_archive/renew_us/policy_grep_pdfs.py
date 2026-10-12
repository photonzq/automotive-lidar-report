"""Locate lidar (and related) wording in statute, bill and budget PDFs, and render the hit pages.

Purpose
    For each PDF in a directory, extracts page text with PyMuPDF only to LOCATE pages that
    mention lidar-related terms, prints page number, term counts and a short context
    window, and renders every hit page to PNG at 160 dpi so that the wording and numbers
    can be read from the page image (the text layer is used for locating only).

Inputs
    pdf_dir : directory holding the PDFs (statutes, bills, committee reports, budget books)
    --terms : optional regex (default lidar|ladar|laser radar|light detection and ranging)
    --render: render hit pages to <pdf_dir>/png/<pdfname>_p<N>.png (default on; --norender to skip)
Outputs
    printed hit list; PNG pages; <pdf_dir>/pdf_hits.csv (file, page, count, context)

Usage:
    python policy_grep_pdfs.py <pdf_dir> [--terms REGEX] [--norender]
"""
import csv
import os
import re
import sys

import pymupdf


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    pdf_dir = argv[1]
    terms = r"lidar|ladar|laser radar|light detection and ranging"
    render = True
    if "--terms" in argv:
        terms = argv[argv.index("--terms") + 1]
    if "--norender" in argv:
        render = False
    pat = re.compile(terms, re.I)
    png_dir = os.path.join(pdf_dir, "png")
    os.makedirs(png_dir, exist_ok=True)
    rows = []
    for fn in sorted(os.listdir(pdf_dir)):
        if not fn.lower().endswith(".pdf"):
            continue
        try:
            d = pymupdf.open(os.path.join(pdf_dir, fn))
        except Exception as e:  # damaged or non-PDF download
            print(fn, "cannot open:", e)
            continue
        total = 0
        for i in range(d.page_count):
            t = d[i].get_text()
            hits = list(pat.finditer(t))
            if not hits:
                continue
            total += len(hits)
            ctx = " | ".join(re.sub(r"\s+", " ", t[max(0, h.start() - 150):h.end() + 150]) for h in hits[:3])
            rows.append((fn, i + 1, len(hits), ctx))
            print(f"{fn} p{i + 1} ({len(hits)}): {ctx[:600]}")
            if render:
                d[i].get_pixmap(dpi=160).save(os.path.join(png_dir, f"{fn[:-4]}_p{i + 1}.png"))
        print(f"== {fn}: {d.page_count} pages, {total} hits")
    with open(os.path.join(pdf_dir, "pdf_hits.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["file", "page", "count", "context"])
        w.writerows(rows)


if __name__ == "__main__":
    main(sys.argv)
