"""Fetch Sony's Japanese AS-DT1 pages (Shift-JIS) and print specification passages.

Used for the Appendix 1 item "Sony AS-DT1" of the automotive perception report.
Sony Japan serves these pages in Shift-JIS, which generic fetchers garble; this
script detects the declared charset, strips scripts and styles, saves plain
text, and prints the passages on price (オープン価格), range conditions
(10万ルクス), SPAD, power (消費電力) and release timing (発売).

Usage
-----
    python asdt1_sony_pages.py OUTDIR

Only a generic browser User-Agent is sent; no cookies, logins or personal data.
"""
import os
import re
import sys

import requests
from bs4 import BeautifulSoup

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124 Safari/537.36",
      "Accept-Language": "ja,en;q=0.8"}
PAGES = {
    "product": "https://www.sony.jp/lidar-depth-sensor/products/AS-DT1/index.html",
    "spec": "https://www.sony.jp/lidar-depth-sensor/products/AS-DT1/spec.html",
    "press_20250411": "https://www.sony.jp/professional/News/Press/20250411/",
}
KEYWORDS = ["オープン価格", "ルクス", "SPAD", "消費電力", "発売", "屋外", "屋内"]


def page_text(url: str) -> str:
    r = requests.get(url, headers=UA, timeout=60)
    m = re.search(rb'charset=["\']?([A-Za-z0-9_\-]+)', r.content[:3000])
    enc = m.group(1).decode() if m else (r.encoding or "utf-8")
    soup = BeautifulSoup(r.content.decode(enc, errors="replace"), "html.parser")
    for s in soup(["script", "style"]):
        s.decompose()
    return re.sub(r"\s+", " ", soup.get_text(" "))


def main() -> None:
    out = sys.argv[1] if len(sys.argv) > 1 else "asdt1_pages"
    os.makedirs(out, exist_ok=True)
    for name, url in PAGES.items():
        t = page_text(url)
        with open(os.path.join(out, name + ".txt"), "w", encoding="utf-8") as f:
            f.write(t)
        print(f"===== {name} ({len(t)} chars)")
        for kw in KEYWORDS:
            for m in list(re.finditer(re.escape(kw), t))[:2]:
                print(f"[{kw}]", t[max(0, m.start() - 120):m.end() + 140])


if __name__ == "__main__":
    main()
