"""Locate pages of a PDF that contain given terms (to choose which rendered pages to read).
Usage: locate_terms.py <pdf> <term> [<term> ...]
Prints, for each term, the 1-based PDF page numbers and a short context snippet."""
import sys

import pymupdf

sys.stdout.reconfigure(encoding="utf-8")
doc = pymupdf.open(sys.argv[1])
terms = sys.argv[2:]
texts = [doc[i].get_text() for i in range(doc.page_count)]
for term in terms:
    print(f"== {term}")
    for i, t in enumerate(texts):
        k = t.find(term)
        n = 0
        while k >= 0 and n < 3:
            snippet = t[max(0, k - 90):k + 110].replace("\n", " ")
            print(f"  p{i + 1}: ...{snippet}...")
            k = t.find(term, k + 1)
            n += 1
