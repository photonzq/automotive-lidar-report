"""R1_partA_E2-E5 source research helper: download documents, locate pages, render pages to PNG.

Usage (run with the Anaconda interpreter):
  python R1A_fetch_render.py download <url> <out_file> [referer]
  python R1A_fetch_render.py info <file.pdf>
  python R1A_fetch_render.py find <file.pdf> <regex> [<regex> ...]
  python R1A_fetch_render.py render <file.pdf> <out_dir> <pages> [dpi]
        <pages> is a 1-based list such as 3,5,7-9
  python R1A_fetch_render.py htmltext <file.html> <out.txt>

Notes:
  - Downloads send a generic browser User-Agent only: no e-mail address, no credentials,
    no cookies.
  - 'find' uses page.get_text() only to locate pages; tables, figures and numbers are read
    from the rendered PNG images (160 dpi by default).
  - All paths are supplied on the command line; <scratch> stands for the researcher's
    temporary folder.
"""
import html
import os
import re
import sys
import urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")


def download(url, out, referer=None):
    headers = {"User-Agent": UA, "Accept": "*/*", "Accept-Language": "en-US,en;q=0.8"}
    if referer:
        headers["Referer"] = referer
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=180) as r:
        data = r.read()
        ctype = r.headers.get("Content-Type", "")
        final = r.geturl()
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "wb") as f:
        f.write(data)
    print(f"saved {len(data)} bytes, content-type={ctype!r}, final-url={final} -> {out}")
    if out.lower().endswith(".pdf") and not data[:5] == b"%PDF-":
        print("WARNING: file does not start with %PDF- (probably an HTML page)")


def info(path):
    import pymupdf
    d = pymupdf.open(path)
    print(f"pages={d.page_count}")
    print("metadata:", d.metadata)


def find(path, patterns):
    import pymupdf
    d = pymupdf.open(path)
    regs = [re.compile(p, re.I) for p in patterns]
    for i in range(d.page_count):
        t = d[i].get_text()
        for rg in regs:
            for m in rg.finditer(t):
                s = max(0, m.start() - 150)
                e = min(len(t), m.end() + 150)
                ctx = t[s:e].replace("\n", " ")
                print(f"[p{i + 1}] /{rg.pattern}/: ...{ctx}...")


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


def render(path, out_dir, spec, dpi=160):
    import pymupdf
    d = pymupdf.open(path)
    os.makedirs(out_dir, exist_ok=True)
    stem = os.path.splitext(os.path.basename(path))[0]
    for p in parse_pages(spec):
        if 1 <= p <= d.page_count:
            out = os.path.join(out_dir, f"{stem}_p{p}.png")
            d[p - 1].get_pixmap(dpi=dpi).save(out)
            print("wrote", out)
        else:
            print(f"page {p} out of range (1..{d.page_count})")


def htmltext(path, out):
    raw = open(path, "rb").read().decode("utf-8", errors="replace")
    raw = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw)
    raw = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</li>|</h\d>|</tr>", "\n", raw)
    txt = re.sub(r"(?s)<[^>]+>", " ", raw)
    txt = html.unescape(txt)
    txt = re.sub(r"[ \t\r\f\v]+", " ", txt)
    txt = re.sub(r"\n\s*\n+", "\n", txt)
    with open(out, "w", encoding="utf-8") as f:
        f.write(txt)
    print(f"wrote {len(txt)} chars -> {out}")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "download":
        download(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None)
    elif cmd == "info":
        info(sys.argv[2])
    elif cmd == "find":
        find(sys.argv[2], sys.argv[3:])
    elif cmd == "render":
        render(sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]) if len(sys.argv) > 5 else 160)
    elif cmd == "htmltext":
        htmltext(sys.argv[2], sys.argv[3])
    else:
        print(__doc__)
