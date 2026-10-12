"""Download public web pages to a local folder and extract their visible text.

Usage:
    python item4_fetch_pages.py OUTDIR URL_LIST_FILE
    python item4_fetch_pages.py OUTDIR --url URL [--name NAME]

URL_LIST_FILE has one entry per line: "name<TAB>url" (lines starting with # are ignored).
For each entry the raw response is saved as OUTDIR/raw/<name>.html and the visible text
(scripts and styles removed, whitespace collapsed) as OUTDIR/text/<name>.txt.
A log line with HTTP status, final URL, byte count and detected encoding is printed.

No login, cookies or credentials are used; pages that answer with a CAPTCHA or a
login wall are saved as-is so that the refusal can be documented, and nothing is retried.
"""
import argparse
import os
import re
import sys
import time

import requests
from bs4 import BeautifulSoup

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
HEADERS = {"User-Agent": UA, "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"}


def visible_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text("\n")
    lines = [re.sub(r"[ \t　\xa0]+", " ", ln).strip() for ln in text.splitlines()]
    return "\n".join(ln for ln in lines if ln)


def fetch(name: str, url: str, outdir: str) -> None:
    os.makedirs(os.path.join(outdir, "raw"), exist_ok=True)
    os.makedirs(os.path.join(outdir, "text"), exist_ok=True)
    try:
        r = requests.get(url, headers=HEADERS, timeout=30, allow_redirects=True)
    except Exception as exc:  # network errors are logged, not raised
        print(f"[ERR] {name}: {exc}")
        return
    enc = r.encoding
    if not enc or enc.lower() in ("iso-8859-1", "ascii"):
        enc = r.apparent_encoding or "utf-8"
    html = r.content.decode(enc, errors="replace")
    with open(os.path.join(outdir, "raw", name + ".html"), "w", encoding="utf-8") as f:
        f.write(html)
    txt = visible_text(html)
    with open(os.path.join(outdir, "text", name + ".txt"), "w", encoding="utf-8") as f:
        f.write(f"SOURCE: {url}\nFINAL: {r.url}\nSTATUS: {r.status_code}\n\n{txt}")
    print(f"[{r.status_code}] {name}: {len(r.content)} bytes, enc={enc}, final={r.url}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("outdir")
    ap.add_argument("listfile", nargs="?")
    ap.add_argument("--url")
    ap.add_argument("--name", default="page")
    ap.add_argument("--delay", type=float, default=1.5)
    a = ap.parse_args()
    if a.url:
        fetch(a.name, a.url, a.outdir)
        return
    with open(a.listfile, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            name, url = line.split("\t", 1)
            fetch(name.strip(), url.strip(), a.outdir)
            time.sleep(a.delay)


if __name__ == "__main__":
    sys.exit(main())
