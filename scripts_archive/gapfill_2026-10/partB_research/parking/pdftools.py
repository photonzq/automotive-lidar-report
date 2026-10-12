"""Small PDF helper built on PyMuPDF.

Usage:
    python pdftools.py info   <file.pdf>
    python pdftools.py grep   <file.pdf> <regex> [<regex> ...]
    python pdftools.py text   <file.pdf> <page1-based> [<page1-based> ...]
    python pdftools.py render <file.pdf> <out_dir> <page1-based or a-b> [...] [--dpi N]

- 'grep' prints 1-based page numbers and the matching line (case-insensitive),
  used only to locate pages worth rendering.
- 'render' writes <out_dir>/<stem>_p<N>.png at the requested dpi (default 160).
"""
import os
import re
import sys

import pymupdf


def parse_pages(tokens, n):
    pages = []
    for t in tokens:
        if "-" in t:
            a, b = t.split("-", 1)
            pages.extend(range(int(a), int(b) + 1))
        else:
            pages.append(int(t))
    return [p for p in pages if 1 <= p <= n]


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    if len(argv) < 3:
        print(__doc__)
        return 1
    cmd, path = argv[1], argv[2]
    doc = pymupdf.open(path)
    n = doc.page_count
    if cmd == "info":
        print(f"pages={n}")
        print(doc.metadata)
        return 0
    if cmd == "grep":
        pats = [re.compile(p, re.I) for p in argv[3:]]
        for i in range(n):
            txt = doc[i].get_text()
            for line in txt.splitlines():
                if any(p.search(line) for p in pats):
                    print(f"p{i + 1}: {line.strip()}")
        return 0
    if cmd == "text":
        for p in parse_pages(argv[3:], n):
            print(f"===== page {p} =====")
            print(doc[p - 1].get_text())
        return 0
    if cmd == "render":
        out_dir = argv[3]
        rest = argv[4:]
        dpi = 160
        if "--dpi" in rest:
            k = rest.index("--dpi")
            dpi = int(rest[k + 1])
            rest = rest[:k] + rest[k + 2:]
        os.makedirs(out_dir, exist_ok=True)
        stem = os.path.splitext(os.path.basename(path))[0]
        for p in parse_pages(rest, n):
            out = os.path.join(out_dir, f"{stem}_p{p}.png")
            doc[p - 1].get_pixmap(dpi=dpi).save(out)
            print(out)
        return 0
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
