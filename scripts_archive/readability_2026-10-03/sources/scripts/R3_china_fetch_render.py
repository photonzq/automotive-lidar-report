"""Fetch a web page or PDF with a generic browser User-Agent (no e-mail, no key),
save it to an output folder, and then either
  * for HTML: decode it (UTF-8 / GBK / GB18030 fallback), strip tags and print
    the lines that match a regex (or the whole text), or
  * for PDF: print page count and metadata, locate pages by regex via
    get_text() and render chosen pages to PNG at 160 dpi with PyMuPDF.

Usage (paths are placeholders; pass your own):
  python R3_china_fetch_render.py fetch <url> <out_dir>/<name>
  python R3_china_fetch_render.py html  <saved.html> [regex] [context_chars]
  python R3_china_fetch_render.py find  <saved.pdf> <regex>
  python R3_china_fetch_render.py render <saved.pdf> <out_dir> <p1,p2,...> [dpi]
Page numbers for 'render' are 1-based.
"""
import html as _html
import re
import sys
import urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def fetch(url, out_path, referer=None):
    headers = {
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/pdf,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    if referer:  # page that embeds an image (some CDNs check it)
        headers["Referer"] = referer
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
        ctype = r.headers.get("Content-Type", "")
    with open(out_path, "wb") as f:
        f.write(data)
    print(f"saved {len(data)} bytes, content-type={ctype!r} -> {out_path}")


def decode(raw):
    m = re.search(rb'charset=["\']?([A-Za-z0-9_\-]+)', raw[:5000])
    encs = []
    if m:
        encs.append(m.group(1).decode("ascii", "ignore"))
    encs += ["utf-8", "gb18030", "gbk"]
    for enc in encs:
        try:
            return raw.decode(enc)
        except (LookupError, UnicodeDecodeError):
            continue
    return raw.decode("utf-8", "replace")


def html_text(path):
    raw = open(path, "rb").read()
    s = decode(raw)
    s = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</li>|</tr>|</h\d>", "\n", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    s = _html.unescape(s)
    s = re.sub(r"[ \t\r\f\v　\xa0]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n", s)
    return s


def cmd_html(path, regex=None, ctx=200):
    t = html_text(path)
    if not regex:
        print(t)
        return
    for m in re.finditer(regex, t):
        a, b = max(0, m.start() - ctx), min(len(t), m.end() + ctx)
        print("...", t[a:b].replace("\n", " / "), "...")
        print("-" * 60)


def cmd_find(pdf, regex):
    import pymupdf
    d = pymupdf.open(pdf)
    print("pages:", d.page_count, "metadata:", d.metadata)
    for i in range(d.page_count):
        txt = d[i].get_text()
        hits = re.findall(regex, txt)
        if hits:
            print(f"page {i + 1}: {len(hits)} hit(s): {hits[:5]}")


def cmd_render(pdf, out_dir, pages, dpi=160):
    import os
    import pymupdf
    d = pymupdf.open(pdf)
    base = os.path.splitext(os.path.basename(pdf))[0]
    for p in pages:
        pix = d[p - 1].get_pixmap(dpi=dpi)
        out = os.path.join(out_dir, f"{base}_p{p}.png")
        pix.save(out)
        print("rendered", out)


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    a = sys.argv[1:]
    if a[0] == "fetch":
        fetch(a[1], a[2], a[3] if len(a) > 3 else None)
    elif a[0] == "html":
        cmd_html(a[1], a[2] if len(a) > 2 else None,
                 int(a[3]) if len(a) > 3 else 200)
    elif a[0] == "find":
        cmd_find(a[1], a[2])
    elif a[0] == "render":
        cmd_render(a[1], a[2], [int(x) for x in a[3].split(",")],
                   int(a[4]) if len(a) > 4 else 160)
