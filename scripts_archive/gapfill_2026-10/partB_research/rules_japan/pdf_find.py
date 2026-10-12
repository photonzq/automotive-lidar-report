"""Locate pages in a PDF that contain given search terms (case-insensitive).

Usage:
    python pdf_find.py FILE.pdf TERM [TERM ...]

Prints, for each term, the 1-based page numbers where it occurs and a short
context snippet for each hit. Text extraction is used only to locate pages;
the pages themselves should then be rendered and read as images.
"""
import re
import sys

import pymupdf


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    doc = pymupdf.open(sys.argv[1])
    print(f"{sys.argv[1]}: {doc.page_count} pages")
    texts = [doc[i].get_text() for i in range(doc.page_count)]
    for term in sys.argv[2:]:
        pat = re.compile(re.escape(term), re.I)
        hits = []
        for i, t in enumerate(texts):
            for m in pat.finditer(t):
                s = max(0, m.start() - 90)
                e = min(len(t), m.end() + 90)
                hits.append((i + 1, " ".join(t[s:e].split())))
        print(f"\n=== '{term}': {len(hits)} hits on pages "
              f"{sorted(set(h[0] for h in hits))}")
        for p, snip in hits[:40]:
            print(f"  p{p}: ...{snip}...")


if __name__ == "__main__":
    main()
