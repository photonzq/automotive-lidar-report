"""R6_C10_part2 source research: download documents, locate and render PDF pages.

Usage (all paths are arguments; nothing user-specific is stored here):
  python R6_pdf_tools.py get    <url> <out_file>
  python R6_pdf_tools.py info   <file.pdf>
  python R6_pdf_tools.py find   <file.pdf> <regex>          (prints matching 1-based page numbers)
  python R6_pdf_tools.py render <file.pdf> <outdir> <pages> [dpi]
        pages: "1-3,7" (1-based); dpi defaults to 160
  python R6_pdf_tools.py clip   <file.pdf> <outdir> <page> <x0> <y0> <x1> <y1> [dpi]
        renders a rectangle (PDF points) of one 1-based page, default 300 dpi
  python R6_pdf_tools.py html2txt <in.html> <out.txt>
        strips scripts, styles and tags from a saved HTML page

Requests use a generic browser User-Agent and carry no e-mail address, key or credentials.
get_text() is used only to locate pages; numbers are read from the rendered images.
"""
import html
import re
import sys
import urllib.request

import pymupdf

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def get(url, out):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
        ctype = r.headers.get("Content-Type", "")
    with open(out, "wb") as f:
        f.write(data)
    print(f"saved {len(data)} bytes, content-type {ctype!r}, starts {data[:8]!r}")


def info(path):
    d = pymupdf.open(path)
    print("pages:", d.page_count)
    for k, v in (d.metadata or {}).items():
        print(f"  {k}: {v}")


def parse_pages(spec):
    out = []
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-")
            out.extend(range(int(a), int(b) + 1))
        elif part:
            out.append(int(part))
    return out


def find(path, pattern):
    d = pymupdf.open(path)
    rx = re.compile(pattern, re.I)
    for i in range(d.page_count):
        hits = rx.findall(d[i].get_text())
        if hits:
            print(f"page {i + 1}: {len(hits)} hit(s)")


def render(path, outdir, spec, dpi=160):
    d = pymupdf.open(path)
    for p in parse_pages(spec):
        if 1 <= p <= d.page_count:
            fn = f"{outdir}/p{p:03d}.png"
            d[p - 1].get_pixmap(dpi=dpi).save(fn)
            print("wrote", fn)


def clip(path, outdir, page, x0, y0, x1, y1, dpi=300):
    d = pymupdf.open(path)
    pg = d[page - 1]
    fn = f"{outdir}/p{page:03d}_clip_{int(x0)}_{int(y0)}.png"
    pg.get_pixmap(dpi=dpi, clip=pymupdf.Rect(x0, y0, x1, y1)).save(fn)
    print("wrote", fn, "page size", pg.rect)


def html2txt(src, dst):
    raw = open(src, "rb").read().decode("utf-8", "replace")
    raw = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", raw)
    raw = re.sub(r"(?i)<br\s*/?>|</p>|</h\d>|</li>|</tr>|</div>", "\n", raw)
    txt = html.unescape(re.sub(r"(?s)<[^>]+>", " ", raw))
    txt = re.sub(r"[ \t\r\f\v]+", " ", txt)
    txt = re.sub(r"\n\s*\n+", "\n\n", txt)
    open(dst, "w", encoding="utf-8").write(txt.strip())
    print("wrote", dst, len(txt), "chars")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "get":
        get(sys.argv[2], sys.argv[3])
    elif cmd == "info":
        info(sys.argv[2])
    elif cmd == "find":
        find(sys.argv[2], sys.argv[3])
    elif cmd == "render":
        render(sys.argv[2], sys.argv[3], sys.argv[4],
               int(sys.argv[5]) if len(sys.argv) > 5 else 160)
    elif cmd == "clip":
        clip(sys.argv[2], sys.argv[3], int(sys.argv[4]),
             *[float(x) for x in sys.argv[5:9]],
             dpi=int(sys.argv[9]) if len(sys.argv) > 9 else 300)
    elif cmd == "html2txt":
        html2txt(sys.argv[2], sys.argv[3])
    else:
        sys.exit("unknown command")
