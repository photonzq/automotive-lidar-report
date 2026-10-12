"""Run Baidu web searches and extract result titles, real URLs and snippets.

Usage:
    python item4_baidu_search.py OUTDIR "query 1" ["query 2" ...] [--pages N]

For every query the raw result page is saved as OUTDIR/baidu/<slug>_p<k>.html and a
plain-text digest (rank, title, real URL from the result's `mu` attribute, source
label and snippet) as OUTDIR/baidu/<slug>_p<k>.txt; the digest is also printed.

The script stops at once, without retrying, if Baidu answers with a security check
(CAPTCHA) page. No cookies, logins or credentials are used.
"""
import argparse
import hashlib
import os
import re
import sys
import time
import urllib.parse

import requests
from bs4 import BeautifulSoup

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
HEADERS = {"User-Agent": UA, "Accept-Language": "zh-CN,zh;q=0.9"}
CAPTCHA_MARKERS = ("百度安全验证", "wappass.baidu.com", "安全验证", "captcha")


def clean(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def parse(html: str):
    soup = BeautifulSoup(html, "html.parser")
    out = []
    for div in soup.select("div.c-container, div.result-op, div.result"):
        mu = div.get("mu") or ""
        h3 = div.find("h3")
        title = clean(h3.get_text(" ")) if h3 else ""
        if not title and not mu:
            continue
        if "recommend_list" in mu or "top.baidu.com" in mu or "nourl" in mu:
            continue
        text = clean(div.get_text(" "))
        out.append({"title": title, "url": mu, "text": text[:600]})
    # de-duplicate nested containers
    seen, res = set(), []
    for r in out:
        key = (r["title"], r["url"])
        if key in seen:
            continue
        seen.add(key)
        res.append(r)
    return res


def search(query: str, outdir: str, pages: int) -> bool:
    os.makedirs(os.path.join(outdir, "baidu"), exist_ok=True)
    slug = hashlib.md5(query.encode("utf-8")).hexdigest()[:10]
    for k in range(pages):
        url = "https://www.baidu.com/s?wd=" + urllib.parse.quote(query) + (f"&pn={10*k}" if k else "")
        r = requests.get(url, headers=HEADERS, timeout=30)
        html = r.content.decode("utf-8", errors="replace")
        base = os.path.join(outdir, "baidu", f"{slug}_p{k}")
        with open(base + ".html", "w", encoding="utf-8") as f:
            f.write(html)
        if any(m in html[:20000] for m in CAPTCHA_MARKERS[:2]) or "wappass" in r.url:
            print(f"!! security check returned for '{query}' - stopping")
            return False
        res = parse(html)
        lines = [f"QUERY: {query}  (page {k+1})  URL: {url}"]
        for i, x in enumerate(res, 1):
            lines.append(f"[{i}] {x['title']}\n    {x['url']}\n    {x['text']}")
        digest = "\n".join(lines)
        with open(base + ".txt", "w", encoding="utf-8") as f:
            f.write(digest)
        print(digest)
        print("-" * 80)
        time.sleep(3)
    return True


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("outdir")
    ap.add_argument("queries", nargs="+")
    ap.add_argument("--pages", type=int, default=1)
    a = ap.parse_args()
    for q in a.queries:
        if not search(q, a.outdir, a.pages):
            sys.exit(2)
        time.sleep(4)


if __name__ == "__main__":
    main()
