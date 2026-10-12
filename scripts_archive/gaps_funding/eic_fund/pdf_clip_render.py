"""Render a horizontal band of a (large) PDF page around a search term.

Usage (run from the eic_fund folder):
    python scripts/pdf_clip_render.py raw/file.pdf PAGE TERM [--above PT] [--below PT] [--dpi N]
PAGE is 1-based. The band spans the full page width, from (term top - above)
to (term bottom + below) in PDF points; it is saved to
png/<pdfstem>_p<PAGE>_<term>.png. Used to read a single row (plus the column
header if requested with a large --above) of a one-page results table.
"""
import argparse
import re
from pathlib import Path

import pymupdf

PNG = Path("png")
PNG.mkdir(exist_ok=True)

ap = argparse.ArgumentParser()
ap.add_argument("pdf")
ap.add_argument("page", type=int)
ap.add_argument("term")
ap.add_argument("--above", type=float, default=40)
ap.add_argument("--below", type=float, default=40)
ap.add_argument("--dpi", type=int, default=160)
ap.add_argument("--x0", type=float, default=None)
ap.add_argument("--x1", type=float, default=None)
a = ap.parse_args()

doc = pymupdf.open(a.pdf)
page = doc[a.page - 1]
rects = page.search_for(a.term)
print("hits:", rects)
if not rects:
    raise SystemExit("term not found")
r = rects[0]
x0 = a.x0 if a.x0 is not None else page.rect.x0
x1 = a.x1 if a.x1 is not None else page.rect.x1
clip = pymupdf.Rect(x0, max(0, r.y0 - a.above), x1, min(page.rect.y1, r.y1 + a.below))
stem = Path(a.pdf).stem[:50]
tag = re.sub(r"[^A-Za-z0-9]+", "_", a.term)[:30]
out = PNG / f"{stem}_p{a.page}_{tag}.png"
pix = page.get_pixmap(dpi=a.dpi, clip=clip)
pix.save(out)
print("saved", out, pix.width, "x", pix.height)
