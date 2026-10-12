"""Locate pages in a PDF that contain given keywords (case-insensitive), to decide which
pages to render.

Usage:
    python scripts/find_pages.py <file.pdf> <kw1> [<kw2> ...] [--ctx 120]

Prints 1-based page numbers with a short context for each hit.
"""
import re
import sys

import pymupdf


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    ctx = 120
    if "--ctx" in args:
        i = args.index("--ctx")
        ctx = int(args[i + 1])
        del args[i:i + 2]
    pdf, kws = args[0], args[1:]
    doc = pymupdf.open(pdf)
    print(f"{pdf}: {doc.page_count} pages")
    for kw in kws:
        print(f"\n=== {kw} ===")
        for p in range(doc.page_count):
            t = doc[p].get_text()
            for m in re.finditer(re.escape(kw), t, flags=re.I):
                a, b = max(0, m.start() - ctx), min(len(t), m.end() + ctx)
                print(f"  p{p + 1}: ...{re.sub(r'\s+', ' ', t[a:b])}...")


if __name__ == "__main__":
    main()
