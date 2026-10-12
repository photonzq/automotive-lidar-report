"""Fetch one web page with a generic browser User-Agent and save its HTML and plain text.

Purpose: collect trade-press and company pages for the passenger-car open items of
Appendix 1 (Rivian, GM, Nissan, Ford) when the default fetcher is refused.
Usage:   python cars_fetch_page.py URL OUTNAME
Outputs: OUTNAME.html and OUTNAME.txt in the current folder (run it inside a data folder).
Date:    2026-10-03
No contact details are sent with the request.
"""
import re
import sys
from html import unescape

import requests

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")


def html_to_text(html):
    """Strip scripts, styles and tags; keep rough paragraph breaks."""
    html = re.sub(r"(?is)<(script|style|noscript).*?</\1>", " ", html)
    html = re.sub(r"(?i)<br\s*/?>|</p>|</h\d>|</li>|</tr>|</div>", "\n", html)
    txt = unescape(re.sub(r"<[^>]+>", " ", html))
    txt = re.sub(r"[ \t\r\f\v]+", " ", txt)
    return re.sub(r"\n\s*\n+", "\n", txt).strip()


def main():
    url, out = sys.argv[1], sys.argv[2]
    r = requests.get(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"}, timeout=40)
    print("status", r.status_code, "len", len(r.text))
    open(out + ".html", "w", encoding="utf-8").write(r.text)
    open(out + ".txt", "w", encoding="utf-8").write(html_to_text(r.text))


if __name__ == "__main__":
    main()
