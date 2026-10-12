"""Download free earnings-call transcript pages and save raw HTML plus extracted text.

For each (label, url) pair below the page is fetched with a generic browser
User-Agent (no cookies, no login), the raw HTML is written to ./transcripts/<label>.html
and the article body text (paragraph by paragraph) to ./transcripts/<label>.txt.
Pages that return an error status are reported and skipped.

Usage (run from the aeva_oem folder):
    python scripts/fetch_transcripts.py
"""
import os
import re
import sys
import urllib.request

from bs4 import BeautifulSoup

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

PAGES = [
    ("fool_q3_2025", "https://www.fool.com/earnings/call-transcripts/2025/11/05/aeva-aeva-q3-2025-earnings-call-transcript/"),
    ("fool_q4_2025", "https://www.fool.com/earnings/call-transcripts/2026/02/26/aeva-aeva-q4-2025-earnings-call-transcript/"),
    ("fool_q1_2026", "https://www.fool.com/earnings/call-transcripts/2026/05/06/aeva-aeva-q1-2026-earnings-call-transcript/"),
    ("fool_q2_2026", "https://www.fool.com/earnings/call-transcripts/2026/08/05/aeva-aeva-q2-2026-earnings-call-transcript/"),
]


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept-Language": "en-US,en;q=0.9"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.status, r.read().decode("utf-8", errors="replace")


def to_text(html):
    soup = BeautifulSoup(html, "lxml")
    for t in soup(["script", "style", "noscript", "header", "footer", "nav"]):
        t.decompose()
    body = soup.find("div", class_=re.compile("article-body")) or soup.find("article") or soup.body
    paras = [p.get_text(" ", strip=True) for p in body.find_all(["p", "h2", "h3", "li"])]
    return "\n\n".join(p for p in paras if p)


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    os.makedirs("transcripts", exist_ok=True)
    pages = PAGES
    if len(sys.argv) > 2:
        pages = [(sys.argv[1], sys.argv[2])]
    for label, url in pages:
        try:
            status, html = fetch(url)
        except Exception as e:  # noqa: BLE001
            print(label, "FAILED", e)
            continue
        open(os.path.join("transcripts", label + ".html"), "w", encoding="utf-8").write(html)
        txt = to_text(html)
        open(os.path.join("transcripts", label + ".txt"), "w", encoding="utf-8").write(url + "\n\n" + txt)
        print(label, status, len(html), len(txt))


if __name__ == "__main__":
    main()
