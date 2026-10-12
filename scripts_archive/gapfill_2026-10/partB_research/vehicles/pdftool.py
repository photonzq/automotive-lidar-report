"""Locate pages in a PDF by keyword and render pages to PNG.

Usage:
    python pdftool.py info PDF
    python pdftool.py grep PDF REGEX [REGEX ...]     (case-insensitive)
    python pdftool.py render PDF OUTDIR PAGES [--dpi 160]
        PAGES is a comma list of 1-based page numbers or ranges, e.g. 3,5-7
    python pdftool.py text PDF PAGES   (print extracted text of pages)

Page numbers here are 1-based PDF page indices, not printed page numbers.
"""
import os
import re
import sys

import pymupdf


def parse_pages(spec):
    pages = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-")
            pages.extend(range(int(a), int(b) + 1))
        else:
            pages.append(int(part))
    return pages


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    cmd = sys.argv[1]
    pdf = sys.argv[2]
    doc = pymupdf.open(pdf)
    if cmd == "info":
        print(f"pages={doc.page_count}")
        print(doc.metadata)
    elif cmd == "grep":
        pats = [re.compile(p, re.I) for p in sys.argv[3:]]
        for i in range(doc.page_count):
            txt = doc[i].get_text()
            for p in pats:
                for m in p.finditer(txt):
                    s = max(0, m.start() - 120)
                    e = min(len(txt), m.end() + 120)
                    snippet = txt[s:e].replace("\n", " ")
                    print(f"[p{i + 1}] /{p.pattern}/ ... {snippet} ...")
    elif cmd == "render":
        outdir = sys.argv[3]
        pages = parse_pages(sys.argv[4])
        dpi = 160
        if "--dpi" in sys.argv:
            dpi = int(sys.argv[sys.argv.index("--dpi") + 1])
        os.makedirs(outdir, exist_ok=True)
        base = os.path.splitext(os.path.basename(pdf))[0]
        for p in pages:
            out = os.path.join(outdir, f"{base}_p{p}.png")
            doc[p - 1].get_pixmap(dpi=dpi).save(out)
            print(out)
    elif cmd == "text":
        for p in parse_pages(sys.argv[3]):
            print(f"===== page {p} =====")
            print(doc[p - 1].get_text())
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
