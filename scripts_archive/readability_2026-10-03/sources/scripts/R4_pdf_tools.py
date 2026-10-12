"""Fetch a file and read PDFs page by page (Round 4, group R4_C7-C7b_F6).

Usage:
  python R4_pdf_tools.py fetch <url> <out_file>
  python R4_pdf_tools.py info <file.pdf>
  python R4_pdf_tools.py find <file.pdf> <regex>
  python R4_pdf_tools.py render <file.pdf> <out_dir> <pages> [dpi]
  python R4_pdf_tools.py clip <file.pdf> <out.png> <page> <x0> <y0> <x1> <y1> [dpi]

Notes:
  - Requests carry only a generic browser User-Agent. No email address, no
    credentials, no API key and no "polite pool" parameter are ever sent.
  - "pages" is a comma list of 1-based pages or ranges, e.g. "1,3-5".
  - get_text() is used only to locate pages; numbers, tables and figures are
    read from the rendered PNGs (160 dpi by default).
  - All paths come from the command line (a scratch folder such as <scratch>/r4);
    nothing is hard-coded.
"""
import re
import sys
import urllib.request

import pymupdf

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def fetch(url, out):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
        ctype = r.headers.get("Content-Type")
        final = r.geturl()
    with open(out, "wb") as f:
        f.write(data)
    print(f"saved {len(data)} bytes; content-type {ctype}; final url {final}; "
          f"starts {data[:8]!r}")


def parse_pages(spec):
    pages = []
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-")
            pages.extend(range(int(a), int(b) + 1))
        elif part:
            pages.append(int(part))
    return pages


def info(path):
    d = pymupdf.open(path)
    print(f"pages: {d.page_count}")
    print(f"metadata: {d.metadata}")
    for i in range(d.page_count):
        first = d[i].get_text().strip().splitlines()[:1]
        print(f"p{i + 1}: {first[0][:100] if first else ''}")


def find(path, pattern):
    d = pymupdf.open(path)
    rx = re.compile(pattern, re.I)
    for i in range(d.page_count):
        text = d[i].get_text()
        hits = [m.start() for m in rx.finditer(text)]
        if hits:
            snips = [text[max(0, h - 60):h + 80].replace("\n", " ") for h in hits[:3]]
            print(f"p{i + 1}: {len(hits)} hit(s)")
            for s in snips:
                print(f"    ...{s}...")


def render(path, out_dir, spec, dpi=160):
    d = pymupdf.open(path)
    stem = re.sub(r"[^A-Za-z0-9_-]", "_", path.replace("\\", "/").split("/")[-1].rsplit(".", 1)[0])
    for p in parse_pages(spec):
        if 1 <= p <= d.page_count:
            out = f"{out_dir}/{stem}_p{p}.png"
            d[p - 1].get_pixmap(dpi=dpi).save(out)
            print(out)


def clip(path, out, page, x0, y0, x1, y1, dpi=300):
    d = pymupdf.open(path)
    pg = d[page - 1]
    r = pg.rect
    rect = pymupdf.Rect(r.x0 + x0 * r.width, r.y0 + y0 * r.height,
                        r.x0 + x1 * r.width, r.y0 + y1 * r.height)
    pg.get_pixmap(dpi=dpi, clip=rect).save(out)
    print(out)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    cmd = sys.argv[1]
    if cmd == "fetch":
        fetch(sys.argv[2], sys.argv[3])
    elif cmd == "info":
        info(sys.argv[2])
    elif cmd == "find":
        find(sys.argv[2], sys.argv[3])
    elif cmd == "render":
        render(sys.argv[2], sys.argv[3], sys.argv[4],
               int(sys.argv[5]) if len(sys.argv) > 5 else 160)
    elif cmd == "clip":
        # x0..y1 are fractions (0-1) of the page width and height
        clip(sys.argv[2], sys.argv[3], int(sys.argv[4]),
             float(sys.argv[5]), float(sys.argv[6]), float(sys.argv[7]), float(sys.argv[8]),
             int(sys.argv[9]) if len(sys.argv) > 9 else 300)
    else:
        sys.exit(__doc__)
