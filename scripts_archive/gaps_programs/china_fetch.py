"""china_fetch.py -- fetch web pages (mostly Chinese automotive sites) and save raw + text copies.

Purpose
    Download a page with a generic browser-like User-Agent (no contact details, no
    cookies, no login), save the raw bytes and a plain-text rendering, and optionally
    print only the lines that match given keywords (with context). Used for the
    foreign-brand-in-China lidar gap items (supplier, trim share, Hesai/RoboSense
    customer identity).

Inputs (command line)
    url             page to fetch
    name            short file stem for the saved copies
    --data DIR      data folder (default: ./data_china, created if missing)
    --grep K1,K2    comma-separated keywords; print matching lines with context
    --ctx N         lines of context around each match (default 2)
    --enc ENC       force a text encoding (otherwise detected)
    --head N        print the first N characters of the text instead of grepping

Outputs
    DIR/<name>.html  raw response body
    DIR/<name>.txt   visible text (script/style removed), one block per line

Date: 2026-10-03
"""
import argparse
import os
import re
import sys

import requests
from bs4 import BeautifulSoup

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")
HDRS = {"User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"}


def fetch(url, enc=None, timeout=30):
    r = requests.get(url, headers=HDRS, timeout=timeout, allow_redirects=True)
    raw = r.content
    if enc:
        text = raw.decode(enc, errors="replace")
    else:
        # prefer meta charset, then apparent encoding
        m = re.search(rb'charset=["\']?([A-Za-z0-9_\-]+)', raw[:4000])
        cs = m.group(1).decode("ascii", "ignore") if m else (r.encoding or r.apparent_encoding)
        if cs and cs.lower() in ("iso-8859-1",):
            cs = r.apparent_encoding or "utf-8"
        try:
            text = raw.decode(cs or "utf-8", errors="replace")
        except LookupError:
            text = raw.decode("utf-8", errors="replace")
    return r.status_code, r.url, raw, text


def visible_text(html):
    soup = BeautifulSoup(html, "lxml")
    for t in soup(["script", "style", "noscript"]):
        t.decompose()
    txt = soup.get_text("\n")
    lines = [re.sub(r"[ \t　\xa0]+", " ", ln).strip() for ln in txt.splitlines()]
    return "\n".join(ln for ln in lines if ln)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("name")
    ap.add_argument("--data", default="data_china")
    ap.add_argument("--grep", default="")
    ap.add_argument("--ctx", type=int, default=2)
    ap.add_argument("--enc", default=None)
    ap.add_argument("--head", type=int, default=0)
    a = ap.parse_args()
    os.makedirs(a.data, exist_ok=True)
    code, final, raw, html = fetch(a.url, a.enc)
    with open(os.path.join(a.data, a.name + ".html"), "wb") as f:
        f.write(raw)
    txt = visible_text(html)
    with open(os.path.join(a.data, a.name + ".txt"), "w", encoding="utf-8") as f:
        f.write(txt)
    sys.stdout.reconfigure(encoding="utf-8")
    print(f"status={code} final={final} bytes={len(raw)} textchars={len(txt)}")
    if a.head:
        print(txt[:a.head])
    if a.grep:
        keys = [k for k in a.grep.split(",") if k]
        lines = txt.splitlines()
        hit = set()
        for i, ln in enumerate(lines):
            if any(k.lower() in ln.lower() for k in keys):
                for j in range(max(0, i - a.ctx), min(len(lines), i + a.ctx + 1)):
                    hit.add(j)
        last = -2
        for j in sorted(hit):
            if j != last + 1:
                print("---")
            print(f"{j}: {lines[j][:400]}")
            last = j


if __name__ == "__main__":
    main()
