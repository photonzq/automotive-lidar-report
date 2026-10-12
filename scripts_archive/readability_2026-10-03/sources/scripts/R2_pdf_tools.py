"""R2 source research helper: download a file, locate PDF pages by text, render pages to PNG.

Usage (run with the Anaconda interpreter):
  python R2_pdf_tools.py download <url> <out_file>
  python R2_pdf_tools.py info <file.pdf>
  python R2_pdf_tools.py find <file.pdf> <regex> [<regex> ...]
  python R2_pdf_tools.py render <file.pdf> <out_dir> <first_page_1based> <last_page_1based> [dpi]
  python R2_pdf_tools.py clip <file.pdf> <out.png> <page_1based> <x0> <y0> <x1> <y1> [dpi]

Notes:
  - Downloads send a generic browser User-Agent only: no e-mail address, cookies or credentials.
  - 'find' uses page.get_text() only to locate pages; numbers are read from the rendered PNGs.
  - 'clip' renders a rectangle (in PDF points) of one page at a higher dpi, for small table text.
  - Paths are given on the command line; <scratch> stands for the researcher's temporary folder.
"""
import re
import sys
import urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/125.0 Safari/537.36")


def download(url, out):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=180) as r:
        data = r.read()
        ctype = r.headers.get("Content-Type", "")
    with open(out, "wb") as f:
        f.write(data)
    print(f"saved {len(data)} bytes, content-type={ctype!r} -> {out}")


def info(path):
    import pymupdf
    d = pymupdf.open(path)
    print(f"pages={d.page_count}")
    md = d.metadata or {}
    for k in ("title", "author", "subject", "creationDate", "modDate"):
        if md.get(k):
            print(f"{k}: {md[k]}")


def find(path, patterns):
    import pymupdf
    d = pymupdf.open(path)
    regs = [re.compile(p, re.I) for p in patterns]
    for i in range(d.page_count):
        t = d[i].get_text()
        for rg in regs:
            for m in rg.finditer(t):
                s = max(0, m.start() - 90)
                e = min(len(t), m.end() + 90)
                snippet = t[s:e].replace("\n", " ")
                print(f"p{i + 1} [{rg.pattern}]: ...{snippet}...")


def render(path, out_dir, first, last, dpi=160):
    import os
    import pymupdf
    os.makedirs(out_dir, exist_ok=True)
    d = pymupdf.open(path)
    last = min(last, d.page_count)
    for i in range(first - 1, last):
        out = os.path.join(out_dir, f"p{i + 1}.png")
        d[i].get_pixmap(dpi=dpi).save(out)
        print(out)


def clip(path, out, page, x0, y0, x1, y1, dpi=300):
    import pymupdf
    d = pymupdf.open(path)
    pg = d[page - 1]
    rect = pymupdf.Rect(x0, y0, x1, y1)
    pg.get_pixmap(dpi=dpi, clip=rect).save(out)
    print(out, "page size:", pg.rect)


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    cmd = sys.argv[1]
    if cmd == "download":
        download(sys.argv[2], sys.argv[3])
    elif cmd == "info":
        info(sys.argv[2])
    elif cmd == "find":
        find(sys.argv[2], sys.argv[3:])
    elif cmd == "render":
        dpi = int(sys.argv[6]) if len(sys.argv) > 6 else 160
        render(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), dpi)
    elif cmd == "clip":
        dpi = int(sys.argv[9]) if len(sys.argv) > 9 else 300
        clip(sys.argv[2], sys.argv[3], int(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]),
             float(sys.argv[7]), float(sys.argv[8]), dpi)
    else:
        raise SystemExit(__doc__)
