"""Fetch a URL with a generic User-Agent.

Usage:
    python -I fget.py page URL OUTNAME [--imgs] [--max N] [--grep REGEX]
        Saves raw bytes to fmcw_raw/OUTNAME.html, text to fmcw_raw/OUTNAME.txt,
        prints text (truncated) and, with --imgs, image URLs with alt text.
    python -I fget.py bin URL OUTPATH
        Saves the raw bytes (PDF, image) to OUTPATH (must be inside the
        teardown_research folder) and prints status, type and size.
    python -I fget.py imgsize URL [URL ...]
        Downloads each image into fmcw_img/ and prints pixel size and bytes.
    python -I fget.py commons TITLE [TITLE ...]
        Queries the Wikimedia Commons API for url, size and extmetadata.
    python -I fget.py commonssearch QUERY
        Lists File: pages matching QUERY on Commons.
"""
import sys
import os
import re
import io
import json
import html
import gzip
import zlib
import hashlib
import urllib.request
import urllib.parse

UA = "report-check/1.0 (research)"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, "fmcw_raw")
IMG = os.path.join(ROOT, "fmcw_img")


def fetch(url, accept="text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": accept,
        "Accept-Language": "en-US,en;q=0.8",
        "Accept-Encoding": "gzip, deflate",
    })
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
        enc = r.headers.get("Content-Encoding", "")
        status = r.status
        ctype = r.headers.get("Content-Type", "")
        final = r.geturl()
    if enc == "gzip":
        data = gzip.decompress(data)
    elif enc == "deflate":
        data = zlib.decompress(data)
    return status, ctype, data, final


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


def decode(data):
    for enc in ("utf-8", "gb18030", "latin-1"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    return data.decode("latin-1", "replace")


def cmd_page(args):
    url, name = args[0], args[1]
    maxc = 60000
    if "--max" in args:
        maxc = int(args[args.index("--max") + 1])
    grep = None
    if "--grep" in args:
        grep = args[args.index("--grep") + 1]
    try:
        status, ctype, data, final = fetch(url)
    except Exception as e:  # noqa: BLE001
        print("FETCH ERROR:", repr(e))
        return
    with open(os.path.join(RAW, name + ".html"), "wb") as f:
        f.write(data)
    txt = decode(data)
    text = to_text(txt)
    with open(os.path.join(RAW, name + ".txt"), "w", encoding="utf-8") as f:
        f.write(text)
    print("STATUS", status, ctype, "bytes", len(data), "final", final)
    m = re.search(r"(?is)<title[^>]*>(.*?)</title>", txt)
    if m:
        print("TITLE:", html.unescape(m.group(1)).strip())
    for prop in ("article:published_time", "article:modified_time", "og:image", "datePublished", "dateModified"):
        for mm in re.finditer(r'(?i)(?:property|name|itemprop)=["\']' + re.escape(prop) + r'["\'][^>]*content=["\']([^"\']+)', txt):
            print("META", prop, "=", mm.group(1))
    for mm in re.finditer(r'"(datePublished|dateModified|uploadDate)"\s*:\s*"([^"]+)"', txt):
        print("JSONLD", mm.group(1), "=", mm.group(2))
    if grep:
        win = 350
        if "--win" in args:
            win = int(args[args.index("--win") + 1])
        last_end = -1
        flat = re.sub(r"\s+", " ", text)
        for m in re.finditer(grep, flat, re.I):
            a = max(0, m.start() - win)
            b = min(len(flat), m.end() + win)
            if a < last_end:
                continue
            print("G> ..." + flat[a:b] + "...\n")
            last_end = b
    else:
        print(text[:maxc])
    if "--imgs" in args:
        print("\n==== IMAGES ====")
        seen = set()
        for m in re.finditer(r"(?i)<img[^>]+>", txt):
            tag = m.group(0)
            for attr in ("src", "data-src", "data-lazy-src", "srcset", "data-srcset", "data-original"):
                mm = re.search(r"\s" + attr + r"""\s*=\s*["']([^"']+)["']""", tag)
                if mm:
                    v = mm.group(1)
                    if v not in seen:
                        seen.add(v)
                        alt = re.search(r"""alt\s*=\s*["']([^"']*)["']""", tag)
                        w = re.search(r"""\swidth\s*=\s*["']?(\d+)""", tag)
                        h = re.search(r"""\sheight\s*=\s*["']?(\d+)""", tag)
                        print(attr, "|", v[:400], "| alt:", (alt.group(1) if alt else ""),
                              "| w,h attr:", (w.group(1) if w else "-"), (h.group(1) if h else "-"))


def inside_root(path):
    ap = os.path.abspath(path)
    return ap.startswith(os.path.abspath(ROOT))


def cmd_bin(args):
    url, out = args[0], args[1]
    if not inside_root(out):
        print("REFUSED: output outside research folder")
        return
    try:
        status, ctype, data, final = fetch(url, accept="*/*")
    except Exception as e:  # noqa: BLE001
        print("FETCH ERROR:", repr(e))
        return
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "wb") as f:
        f.write(data)
    print("STATUS", status, ctype, "bytes", len(data), "final", final, "->", out)


def cmd_imgsize(args):
    try:
        from PIL import Image
    except Exception as e:  # noqa: BLE001
        print("PIL missing", e)
        return
    for url in args:
        try:
            status, ctype, data, final = fetch(url, accept="image/avif,image/webp,image/png,image/jpeg,*/*")
        except Exception as e:  # noqa: BLE001
            print("FETCH ERROR", url, repr(e))
            continue
        h = hashlib.sha1(url.encode()).hexdigest()[:10]
        ext = os.path.splitext(urllib.parse.urlparse(final).path)[1][:6] or ".bin"
        fn = os.path.join(IMG, h + ext)
        with open(fn, "wb") as f:
            f.write(data)
        try:
            im = Image.open(io.BytesIO(data))
            size = im.size
            fmt = im.format
        except Exception as e:  # noqa: BLE001
            size, fmt = None, "unreadable:" + repr(e)[:80]
        print("IMG", url, "| status", status, "|", ctype, "| bytes", len(data), "| px", size, "|", fmt, "| saved", fn)


def commons_api(params):
    base = "https://commons.wikimedia.org/w/api.php?"
    url = base + urllib.parse.urlencode(params)
    status, ctype, data, final = fetch(url, accept="application/json")
    return json.loads(data.decode("utf-8"))


def cmd_commons(args):
    titles = "|".join(args)
    js = commons_api({
        "action": "query", "format": "json", "titles": titles,
        "prop": "imageinfo", "iiprop": "url|size|extmetadata",
    })
    for pid, page in js.get("query", {}).get("pages", {}).items():
        print("TITLE:", page.get("title"))
        for ii in page.get("imageinfo", []):
            print("  url:", ii.get("url"))
            print("  descriptionurl:", ii.get("descriptionurl"))
            print("  size:", ii.get("width"), "x", ii.get("height"), "bytes", ii.get("size"))
            em = ii.get("extmetadata", {})
            for k in ("LicenseShortName", "License", "LicenseUrl", "Artist", "Credit", "DateTimeOriginal", "ImageDescription", "UsageTerms", "Copyrighted", "AttributionRequired"):
                if k in em:
                    v = re.sub(r"<[^>]+>", "", str(em[k].get("value", "")))
                    print("  ", k, ":", v[:400])


def cmd_commonssearch(args):
    q = " ".join(args)
    js = commons_api({
        "action": "query", "format": "json", "list": "search",
        "srsearch": q, "srnamespace": "6", "srlimit": "50",
    })
    for r in js.get("query", {}).get("search", []):
        print(r.get("title"), "|", re.sub(r"<[^>]+>", "", r.get("snippet", ""))[:200])


def cmd_lgrep(args):
    name, pat = args[0], args[1]
    win = 350
    if "--win" in args:
        win = int(args[args.index("--win") + 1])
    with open(os.path.join(RAW, name + ".txt"), encoding="utf-8") as f:
        flat = re.sub(r"\s+", " ", f.read())
    last_end = -1
    for m in re.finditer(pat, flat, re.I):
        a = max(0, m.start() - win)
        b = min(len(flat), m.end() + win)
        if a < last_end:
            continue
        print("G> ..." + flat[a:b] + "...\n")
        last_end = b


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
    sub = sys.argv[1]
    args = sys.argv[2:]
    {"page": cmd_page, "bin": cmd_bin, "imgsize": cmd_imgsize,
     "commons": cmd_commons, "commonssearch": cmd_commonssearch,
     "lgrep": cmd_lgrep}[sub](args)


if __name__ == "__main__":
    main()
