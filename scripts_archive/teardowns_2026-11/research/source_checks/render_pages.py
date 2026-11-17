"""Render chosen PDF pages to PNG for reading.

Usage: render_pages.py <file.pdf> <out_dir> <dpi> <page> [<page> ...]   (pages are 1-based)
"""
import sys
from pathlib import Path

import pymupdf

pdf, out, dpi = sys.argv[1], Path(sys.argv[2]), int(sys.argv[3])
out.mkdir(parents=True, exist_ok=True)
doc = pymupdf.open(pdf)
print("pages:", doc.page_count)
for p in map(int, sys.argv[4:]):
    pix = doc[p - 1].get_pixmap(dpi=dpi)
    name = out / f"{Path(pdf).stem}_p{p}.png"
    pix.save(name)
    print(name.name, pix.width, pix.height)
