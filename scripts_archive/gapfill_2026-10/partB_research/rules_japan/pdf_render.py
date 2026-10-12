"""Render selected pages of a PDF to PNG.

Usage:
    python pdf_render.py FILE.pdf OUTPREFIX DPI PAGE [PAGE ...]

PAGE numbers are 1-based. Output files are OUTPREFIX_p<PAGE>.png.
"""
import sys

import pymupdf


def main():
    if len(sys.argv) < 5:
        sys.exit(__doc__)
    pdf, prefix, dpi = sys.argv[1], sys.argv[2], int(sys.argv[3])
    doc = pymupdf.open(pdf)
    for p in sys.argv[4:]:
        n = int(p)
        if not 1 <= n <= doc.page_count:
            print(f"skip page {n}: out of range 1..{doc.page_count}")
            continue
        out = f"{prefix}_p{n}.png"
        doc[n - 1].get_pixmap(dpi=dpi).save(out)
        print(out)


if __name__ == "__main__":
    main()
