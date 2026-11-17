"""Render pages of a PDF to PNG with PyMuPDF.

Usage: python -I render_pdf.py PDF OUTPREFIX DPI [first last]
PyMuPDF lives in the user site-packages, which -I hides, so add that path
explicitly (the script directory is separate from the download directory).
"""
import os
import sys

sys.path.append(os.path.expandvars(r"%APPDATA%\Python\Python313\site-packages"))
import pymupdf  # noqa: E402

pdf, prefix, dpi = sys.argv[1], sys.argv[2], int(sys.argv[3])
d = pymupdf.open(pdf)
first = int(sys.argv[4]) if len(sys.argv) > 4 else 1
last = int(sys.argv[5]) if len(sys.argv) > 5 else d.page_count
print("pages", d.page_count, "metadata", d.metadata)
for i in range(first - 1, min(last, d.page_count)):
    out = f"{prefix}_p{i + 1}.png"
    d[i].get_pixmap(dpi=dpi).save(out)
    print("saved", out)
