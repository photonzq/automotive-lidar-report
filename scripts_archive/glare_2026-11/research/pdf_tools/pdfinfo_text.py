"""Print page count and the first N characters of text for given pages of a PDF.
Usage: python pdfinfo_text.py <pdf> [first_page_1based] [last_page_1based] [nchars]
Used only to locate pages worth rendering.
"""
import sys
import pymupdf

pdf = sys.argv[1]
d = pymupdf.open(pdf)
first = int(sys.argv[2]) if len(sys.argv) > 2 else 1
last = int(sys.argv[3]) if len(sys.argv) > 3 else min(d.page_count, 3)
nchars = int(sys.argv[4]) if len(sys.argv) > 4 else 1500
print("page_count", d.page_count)
for i in range(first - 1, min(last, d.page_count)):
    t = d[i].get_text()
    print("=" * 20, "page", i + 1, "=" * 20)
    print(t[:nchars])
