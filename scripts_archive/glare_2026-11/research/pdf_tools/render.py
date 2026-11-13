"""Render pages of a PDF to PNG.
Usage: python render.py <pdf> <outdir> <prefix> <first_page_1based> <last_page_1based> [dpi]
"""
import os
import sys
import pymupdf

pdf, outdir, prefix = sys.argv[1], sys.argv[2], sys.argv[3]
first, last = int(sys.argv[4]), int(sys.argv[5])
dpi = int(sys.argv[6]) if len(sys.argv) > 6 else 160
os.makedirs(outdir, exist_ok=True)
d = pymupdf.open(pdf)
for i in range(first - 1, min(last, d.page_count)):
    out = os.path.join(outdir, f"{prefix}_p{i + 1}.png")
    d[i].get_pixmap(dpi=dpi).save(out)
    print(out)
