"""Render every page of the given PDFs to PNG (dpi configurable) and dump the
plain text of each page to a .txt file, for locating passages.

Usage:
    python render_pdf_pages.py <dpi> <file1.pdf> [<file2.pdf> ...]

Outputs <stem>_p<N>.png and <stem>.txt in the same folder as each PDF.
"""
import os
import sys

import pymupdf


def main():
    dpi = int(sys.argv[1])
    for pdf in sys.argv[2:]:
        doc = pymupdf.open(pdf)
        stem = os.path.splitext(pdf)[0]
        print(f"{pdf}: {doc.page_count} page(s)")
        with open(stem + ".txt", "w", encoding="utf-8") as fh:
            for i in range(doc.page_count):
                page = doc[i]
                page.get_pixmap(dpi=dpi).save(f"{stem}_p{i + 1}.png")
                fh.write(f"\n===== PAGE {i + 1} =====\n")
                fh.write(page.get_text())


if __name__ == "__main__":
    main()
