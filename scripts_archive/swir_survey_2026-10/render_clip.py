"""Render a rectangular clip of one PDF page at a chosen dpi.
Usage: render_clip.py <pdf> <page_1based> <x0_frac> <y0_frac> <x1_frac> <y1_frac> <dpi> <out.png>
The clip is given as fractions of the page width and height."""
import sys

import pymupdf

pdf, page, x0, y0, x1, y1, dpi, out = sys.argv[1:9]
doc = pymupdf.open(pdf)
p = doc[int(page) - 1]
r = p.rect
clip = pymupdf.Rect(r.x0 + float(x0) * r.width, r.y0 + float(y0) * r.height,
                    r.x0 + float(x1) * r.width, r.y0 + float(y1) * r.height)
p.get_pixmap(dpi=int(dpi), clip=clip).save(out)
print(out, "page", page, "of", doc.page_count)
