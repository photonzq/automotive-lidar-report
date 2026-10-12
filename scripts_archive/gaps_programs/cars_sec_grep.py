"""Download SEC documents (HTML exhibits) and print the context around each regex match.

Purpose: read Rivian, Hesai, MicroVision and Luminar exhibits for supplier and customer
mentions (Appendix 1 passenger-car and China-JV items).
Usage:   python cars_sec_grep.py REGEX URL [URL ...]
Outputs: saves each document as sec_<basename> in the current folder and prints
         about 400 characters either side of each match.
Date:    2026-10-03
"""
import os
import re
import sys
from html import unescape

import requests

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) research-script"


def text_of(html):
    html = re.sub(r"(?is)<(script|style).*?</\1>", " ", html)
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", html)))


def main():
    pat = re.compile(sys.argv[1], re.I)
    for url in sys.argv[2:]:
        fn = "sec_" + os.path.basename(url)
        if not os.path.exists(fn):
            r = requests.get(url, headers={"User-Agent": UA}, timeout=60)
            open(fn, "w", encoding="utf-8").write(r.text)
        t = text_of(open(fn, encoding="utf-8").read())
        print("=====", url)
        for m in pat.finditer(t):
            print("...", t[max(0, m.start() - 400): m.end() + 400], "...\n")


if __name__ == "__main__":
    main()
