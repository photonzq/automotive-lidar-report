"""List pages of a PDF whose extracted text contains any of the given (case-insensitive) terms.
Usage: python findtext.py <pdf> term1 [term2 ...]
Used only to locate pages worth rendering.
"""
import sys
import pymupdf

pdf = sys.argv[1]
terms = [t.lower() for t in sys.argv[2:]]
d = pymupdf.open(pdf)
print("page_count", d.page_count)
for i in range(d.page_count):
    t = d[i].get_text().lower()
    hits = [term for term in terms if term in t]
    if hits:
        print(i + 1, hits)
