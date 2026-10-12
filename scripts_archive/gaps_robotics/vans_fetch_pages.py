"""Fetch web pages (HTML or PDF) and save raw bytes plus extracted plain text.

Used for the China delivery-van open item of the automotive perception report
(Appendix 1, section B4a): product pages, press releases, regulations and news
articles in Chinese and English are saved so that quotes can be checked
against the original wording rather than search-engine summaries.

Usage
-----
    python vans_fetch_pages.py OUTDIR URL [URL ...]
    python vans_fetch_pages.py OUTDIR --list urls.txt

For each URL the script writes ``<slug>.raw`` (bytes as served) and, for HTML,
``<slug>.txt`` (visible text, charset detected from headers or <meta>). PDFs
are saved as ``<slug>.pdf``; read them by rendering pages to PNG.

Only a generic browser User-Agent is sent: no cookies, logins or personal data.
"""
import hashlib
import os
import re
import sys
import time

import requests
from bs4 import BeautifulSoup

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124 Safari/537.36",
      "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"}


def slug(url: str) -> str:
    """Short, filesystem-safe name derived from the URL."""
    base = re.sub(r"^https?://", "", url)
    base = re.sub(r"[^A-Za-z0-9._-]+", "_", base)[:80]
    return base + "_" + hashlib.md5(url.encode()).hexdigest()[:6]


def decode(resp: requests.Response) -> str:
    """Decode HTML using the declared charset, else <meta>, else apparent encoding."""
    enc = None
    ctype = resp.headers.get("content-type", "")
    m = re.search(r"charset=([\w-]+)", ctype, re.I)
    if m:
        enc = m.group(1)
    if not enc:
        m = re.search(rb"<meta[^>]+charset=[\"']?([\w-]+)", resp.content[:4000], re.I)
        if m:
            enc = m.group(1).decode()
    if not enc:
        enc = resp.apparent_encoding or "utf-8"
    return resp.content.decode(enc, errors="replace")


def fetch(url: str, out: str) -> str:
    """Download one URL into ``out``; return the path of the text or PDF file."""
    os.makedirs(out, exist_ok=True)
    s = slug(url)
    r = requests.get(url, headers=UA, timeout=(10, 25))
    r.raise_for_status()
    if r.content[:5] == b"%PDF-" or "pdf" in r.headers.get("content-type", ""):
        path = os.path.join(out, s + ".pdf")
        with open(path, "wb") as f:
            f.write(r.content)
        return path
    with open(os.path.join(out, s + ".raw"), "wb") as f:
        f.write(r.content)
    html = decode(r)
    soup = BeautifulSoup(html, "html.parser")
    for t in soup(["script", "style", "noscript"]):
        t.decompose()
    text = re.sub(r"\n\s*\n+", "\n\n", soup.get_text("\n"))
    path = os.path.join(out, s + ".txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(url + "\n\n" + text)
    return path


def main() -> None:
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    out = sys.argv[1]
    urls = sys.argv[2:]
    if urls[0] == "--list":
        with open(urls[1], encoding="utf-8") as f:
            urls = [u.strip() for u in f if u.strip() and not u.startswith("#")]
    for u in urls:
        try:
            p = fetch(u, out)
            print("OK ", u, "->", os.path.basename(p), flush=True)
        except Exception as e:  # report and continue with the next URL
            print("ERR", u, type(e).__name__, str(e)[:120], flush=True)
        time.sleep(1.0)


if __name__ == "__main__":
    main()
