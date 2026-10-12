"""R8_C9a_inband: download a file with a generic User-Agent (no email, no key),
print PDF page count and metadata, locate pages by regex via get_text(), and
render chosen pages (160 dpi) or a clipped region (300 dpi) to PNG with PyMuPDF.

Usage:
  python R8_pdf_tools.py get  <url> <out_path> [referer]
  python R8_pdf_tools.py info <pdf>
  python R8_pdf_tools.py find <pdf> <regex> [context_chars]
  python R8_pdf_tools.py render <pdf> <out_dir> <pages, 1-based, e.g. 1,3,5-7> [dpi]
  python R8_pdf_tools.py clip <pdf> <out_png> <page 1-based> <x0> <y0> <x1> <y1> [dpi]
"""
import re
import sys
import urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def get(url, out, referer=None):
    headers = {"User-Agent": UA, "Accept": "*/*"}
    if referer:
        headers["Referer"] = referer
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=90) as r:
        data = r.read()
        ctype = r.headers.get("Content-Type")
    with open(out, "wb") as f:
        f.write(data)
    print(f"saved {len(data)} bytes, content-type {ctype}, to {out}")


def parse_pages(spec):
    pages = []
    for part in spec.split(","):
        if "-" in part:
            a, b = part.split("-")
            pages.extend(range(int(a), int(b) + 1))
        else:
            pages.append(int(part))
    return pages


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    cmd = sys.argv[1]
    if cmd == "get":
        get(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None)
        return
    import pymupdf
    if cmd == "info":
        d = pymupdf.open(sys.argv[2])
        print("pages:", d.page_count)
        for k, v in (d.metadata or {}).items():
            print(f"  {k}: {v}")
    elif cmd == "find":
        d = pymupdf.open(sys.argv[2])
        rx = re.compile(sys.argv[3], re.I)
        ctx = int(sys.argv[4]) if len(sys.argv) > 4 else 80
        for i in range(d.page_count):
            t = d[i].get_text()
            for m in rx.finditer(t):
                s = max(0, m.start() - ctx)
                e = min(len(t), m.end() + ctx)
                snippet = t[s:e].replace("\n", " | ")
                print(f"p{i + 1}: ...{snippet}...")
    elif cmd == "render":
        d = pymupdf.open(sys.argv[2])
        out_dir = sys.argv[3]
        dpi = int(sys.argv[5]) if len(sys.argv) > 5 else 160
        for p in parse_pages(sys.argv[4]):
            if 1 <= p <= d.page_count:
                fn = f"{out_dir}/p{p}.png"
                d[p - 1].get_pixmap(dpi=dpi).save(fn)
                print("wrote", fn)
    elif cmd == "clip":
        d = pymupdf.open(sys.argv[2])
        out_png = sys.argv[3]
        p = int(sys.argv[4])
        x0, y0, x1, y1 = (float(v) for v in sys.argv[5:9])
        dpi = int(sys.argv[9]) if len(sys.argv) > 9 else 300
        page = d[p - 1]
        page.get_pixmap(dpi=dpi, clip=pymupdf.Rect(x0, y0, x1, y1)).save(out_png)
        print("wrote", out_png, "page size", page.rect)


if __name__ == "__main__":
    main()
