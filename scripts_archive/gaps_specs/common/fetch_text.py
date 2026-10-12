"""Download public web pages and print their readable text.

Used to read press releases, trade-press articles and product pages in
English, Chinese and Japanese. Each page is saved as HTML; scripts and styles
are stripped; tags are removed; whitespace is collapsed. An optional keyword
list restricts the printout to windows of text around each keyword. Image
URLs found in the page are listed, so that figures can be fetched and viewed.

No login, no cookies beyond the session, no contact details are sent; a
generic browser User-Agent is used.

Usage : python fetch_text.py [-k kw1,kw2] [-w 600] <url> [<url> ...]
Output: <name>.html files in GAPS_SPECS_RAW (default "."); text on stdout
        (UTF-8).
"""
import argparse
import html
import os
import re
import sys

import requests

OUT = os.environ.get("GAPS_SPECS_RAW", ".")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
sys.stdout.reconfigure(encoding="utf-8")


def page_text(raw):
    t = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
    t = re.sub(r"<style.*?</style>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<(br|p|div|li|tr|h\d)[^>]*>", "\n", t, flags=re.I)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    t = re.sub(r"[ \t\r\f\v]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n", t)
    return t


def safe_name(url):
    return re.sub(r"[^A-Za-z0-9._-]+", "_", url.split("://", 1)[-1])[:150]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-k", "--keywords", default="")
    ap.add_argument("-w", "--window", type=int, default=600)
    ap.add_argument("--maxchars", type=int, default=12000)
    ap.add_argument("urls", nargs="+")
    a = ap.parse_args()
    kws = [k for k in a.keywords.split(",") if k]
    for url in a.urls:
        try:
            r = requests.get(url, headers={"User-Agent": UA}, timeout=60)
        except Exception as exc:
            print("#####", url, "failed:", exc)
            continue
        if r.encoding is None or r.encoding.lower() in ("iso-8859-1", "ascii"):
            r.encoding = r.apparent_encoding
        raw = r.text
        with open(os.path.join(OUT, safe_name(url) + ".html"), "w", encoding="utf-8") as fh:
            fh.write(raw)
        txt = page_text(raw)
        print("#####", url, r.status_code, "chars:", len(txt))
        if kws:
            for kw in kws:
                for m in re.finditer(re.escape(kw), txt, flags=re.I):
                    s = max(0, m.start() - a.window)
                    print(f"--- [{kw}] ...{txt[s:m.end() + a.window]}...")
        else:
            print(txt[: a.maxchars])
        imgs = re.findall(r"<img[^>]+src=[\"']([^\"']+)[\"']", raw, flags=re.I)
        print("IMAGES:", imgs[:60])


if __name__ == "__main__":
    main()
