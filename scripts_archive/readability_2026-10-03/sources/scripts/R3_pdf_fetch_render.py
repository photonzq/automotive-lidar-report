"""Download a PDF (generic browser User-Agent, no email or credentials) and render pages.

Usage:
  python R3_pdf_fetch_render.py fetch <url> <out.pdf>
  python R3_pdf_fetch_render.py info <file.pdf>                  # page count and first line per page
  python R3_pdf_fetch_render.py find <file.pdf> <regex>          # pages whose text matches (locating only)
  python R3_pdf_fetch_render.py render <file.pdf> <outdir> <pages> [dpi]
      pages: comma list of 1-based pages or ranges, e.g. "1,3-5"; dpi defaults to 160

Text extraction is used only to locate pages; tables and figures are read from the PNGs.
Paths are given on the command line (scratch folder, e.g. <scratch>/r3), never hard-coded.
"""
import re
import sys
import urllib.request

import pymupdf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def fetch(url, out):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=90) as r:
        data = r.read()
        ctype = r.headers.get("Content-Type")
    with open(out, "wb") as f:
        f.write(data)
    print(f"saved {len(data)} bytes, content-type {ctype}, starts {data[:8]!r}")


def parse_pages(spec):
    pages = []
    for part in spec.split(","):
        if "-" in part:
            a, b = part.split("-")
            pages.extend(range(int(a), int(b) + 1))
        else:
            pages.append(int(part))
    return pages


def info(pdf):
    d = pymupdf.open(pdf)
    print("page_count", d.page_count)
    print("metadata", d.metadata)
    for i, p in enumerate(d):
        t = " ".join(p.get_text().split())[:150]
        print(i + 1, t)


def find(pdf, rx):
    d = pymupdf.open(pdf)
    pat = re.compile(rx, re.I)
    for i, p in enumerate(d):
        t = p.get_text()
        for m in pat.finditer(t):
            s = max(0, m.start() - 80)
            print(f"p{i + 1}: ...{' '.join(t[s:m.end() + 80].split())}...")


def render(pdf, outdir, spec, dpi=160):
    d = pymupdf.open(pdf)
    for n in parse_pages(spec):
        if 1 <= n <= d.page_count:
            out = f"{outdir}/p{n}.png"
            d[n - 1].get_pixmap(dpi=dpi).save(out)
            print("wrote", out)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "fetch":
        fetch(sys.argv[2], sys.argv[3])
    elif cmd == "info":
        info(sys.argv[2])
    elif cmd == "find":
        find(sys.argv[2], sys.argv[3])
    elif cmd == "render":
        render(sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]) if len(sys.argv) > 5 else 160)
