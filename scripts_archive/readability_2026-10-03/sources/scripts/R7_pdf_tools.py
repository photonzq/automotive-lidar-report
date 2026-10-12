"""R7 source research helper: download a PDF, locate pages by text, render pages to PNG.

Usage (run with the Anaconda interpreter):
  python R7_pdf_tools.py download <url> <out.pdf>
  python R7_pdf_tools.py find <file.pdf> <regex> [<regex> ...]
  python R7_pdf_tools.py render <file.pdf> <out_dir> <first_page_1based> <last_page_1based> [dpi]
  python R7_pdf_tools.py info <file.pdf>

Notes:
  - Downloads use a generic browser User-Agent and send no e-mail address or credentials.
  - 'find' uses page.get_text() only to locate pages; numbers are read from the rendered PNGs.
  - Paths are supplied on the command line; placeholders such as <scratch> stand for the
    researcher's temporary folder.
"""
import re
import sys
import urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def download(url, out):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
        ctype = r.headers.get("Content-Type", "")
    with open(out, "wb") as f:
        f.write(data)
    print(f"saved {len(data)} bytes, content-type={ctype!r} -> {out}")
    if not data[:5] == b"%PDF-":
        print("WARNING: file does not start with %PDF- (may be an HTML page)")


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
                s = max(0, m.start() - 120)
                e = min(len(t), m.end() + 120)
                snippet = t[s:e].replace("\n", " ")
                print(f"p{i + 1} [{rg.pattern}]: ...{snippet}...")


def render(path, out_dir, first, last, dpi=160):
    import os
    import pymupdf
    d = pymupdf.open(path)
    os.makedirs(out_dir, exist_ok=True)
    stem = os.path.splitext(os.path.basename(path))[0]
    last = min(last, d.page_count)
    for i in range(first - 1, last):
        out = os.path.join(out_dir, f"{stem}_p{i + 1}.png")
        d[i].get_pixmap(dpi=dpi).save(out)
        print(out)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "download":
        download(sys.argv[2], sys.argv[3])
    elif cmd == "find":
        find(sys.argv[2], sys.argv[3:])
    elif cmd == "render":
        dpi = int(sys.argv[6]) if len(sys.argv) > 6 else 160
        render(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), dpi)
    elif cmd == "info":
        info(sys.argv[2])
    else:
        raise SystemExit("unknown command")
