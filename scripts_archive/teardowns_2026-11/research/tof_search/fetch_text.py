"""Fetch a web page with a generic User-Agent, save the raw HTML, and print
readable text plus image URLs.

Usage:
    python -I fetch_text.py URL OUTNAME [--imgs] [--maxchars N]

The raw HTML goes to ../raw/OUTNAME.html and the extracted text to
../raw/OUTNAME.txt (paths relative to this script's folder).
"""
import sys
import os
import re
import html
import urllib.request
import gzip
import zlib

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) report-check/1.0 (research)"


def fetch(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6",
        "Accept-Encoding": "gzip, deflate",
    })
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
        enc = r.headers.get("Content-Encoding", "")
        status = r.status
        ctype = r.headers.get("Content-Type", "")
    if enc == "gzip":
        data = gzip.decompress(data)
    elif enc == "deflate":
        data = zlib.decompress(data)
    return status, ctype, data


def to_text(raw):
    s = raw
    s = re.sub(r"(?is)<script.*?</script>", " ", s)
    s = re.sub(r"(?is)<style.*?</style>", " ", s)
    s = re.sub(r"(?is)<noscript.*?</noscript>", " ", s)
    s = re.sub(r"(?i)<br\s*/?>", "\n", s)
    s = re.sub(r"(?i)</(p|div|h[1-6]|li|tr|figcaption|section|article)>", "\n", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t\r\f\v]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n", s)
    return s.strip()


def main():
    url = sys.argv[1]
    name = sys.argv[2]
    want_imgs = "--imgs" in sys.argv
    maxchars = 200000
    if "--maxchars" in sys.argv:
        maxchars = int(sys.argv[sys.argv.index("--maxchars") + 1])
    here = os.path.dirname(os.path.abspath(__file__))
    rawdir = os.path.join(os.path.dirname(here), "raw")
    os.makedirs(rawdir, exist_ok=True)
    try:
        status, ctype, data = fetch(url)
    except Exception as e:  # noqa: BLE001
        print("FETCH ERROR:", repr(e))
        return
    with open(os.path.join(rawdir, name + ".html"), "wb") as f:
        f.write(data)
    txt = None
    for enc in ("utf-8", "gb18030", "latin-1"):
        try:
            txt = data.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    text = to_text(txt)
    with open(os.path.join(rawdir, name + ".txt"), "w", encoding="utf-8") as f:
        f.write(text)
    print("STATUS", status, ctype, "bytes", len(data))
    print(text[:maxchars])
    if want_imgs:
        print("\n==== IMAGES ====")
        seen = set()
        for m in re.finditer(r"""(?i)<img[^>]+>""", txt):
            tag = m.group(0)
            for attr in ("src", "data-src", "data-lazy-src", "srcset", "data-original"):
                mm = re.search(attr + r"""\s*=\s*["']([^"']+)["']""", tag)
                if mm:
                    v = mm.group(1)
                    if v not in seen:
                        seen.add(v)
                        alt = re.search(r"""alt\s*=\s*["']([^"']*)["']""", tag)
                        print(attr, "|", v, "| alt:", alt.group(1) if alt else "")


if __name__ == "__main__":
    main()
