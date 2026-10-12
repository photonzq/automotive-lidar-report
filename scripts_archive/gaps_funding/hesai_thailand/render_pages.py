"""Render selected PDF pages to PNG with PyMuPDF.

Usage:
    python scripts/render_pages.py <file.pdf> <page,page,...> [--dpi 160] [--out png]

Pages are 1-based (as printed by hkex_download.py / find_pages.py). PNGs are saved as
<out>/<pdf-stem>_p<N>.png.
"""
import os
import sys

import pymupdf


def main():
    args = sys.argv[1:]
    pdf = args[0]
    pages = [int(p) for p in args[1].split(",") if p.strip()]
    dpi = 160
    out = "png"
    if "--dpi" in args:
        dpi = int(args[args.index("--dpi") + 1])
    if "--out" in args:
        out = args[args.index("--out") + 1]
    os.makedirs(out, exist_ok=True)
    doc = pymupdf.open(pdf)
    stem = os.path.splitext(os.path.basename(pdf))[0]
    for p in pages:
        if p < 1 or p > doc.page_count:
            print("skip", p)
            continue
        path = os.path.join(out, f"{stem}_p{p}.png")
        doc[p - 1].get_pixmap(dpi=dpi).save(path)
        print(path)


if __name__ == "__main__":
    main()
