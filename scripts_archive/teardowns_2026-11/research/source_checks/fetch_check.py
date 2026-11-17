"""Fetch pages and print the paragraphs that contain given keywords, to check teardown claims at their sources.

Usage: fetch_check.py <jobs.json> <out.txt>
jobs.json: list of {"url": ..., "keys": [...]} ; prints status, title and matching text blocks (each cut to 700 chars).
"""
import json
import re
import sys

import requests
from bs4 import BeautifulSoup

UA = {"User-Agent": "report-check/1.0 (research)"}
jobs = json.load(open(sys.argv[1], encoding="utf-8"))
out = open(sys.argv[2], "w", encoding="utf-8")
CUT = int(sys.argv[3]) if len(sys.argv) > 3 else 700
for job in jobs:
    url, keys = job["url"], job["keys"]
    try:
        r = requests.get(url, headers=UA, timeout=40)
        out.write(f"\n===== {url}\nHTTP {r.status_code}\n")
        if r.status_code != 200:
            continue
        r.encoding = r.apparent_encoding if not r.encoding or r.encoding.lower() == "iso-8859-1" else r.encoding
        soup = BeautifulSoup(r.text, "html.parser")
        for s in soup(["script", "style", "noscript"]):
            s.decompose()
        title = soup.title.get_text(strip=True) if soup.title else ""
        out.write(f"TITLE: {title}\n")
        blocks = []
        for el in soup.find_all(["p", "li", "h1", "h2", "h3", "td", "div"]):
            if el.find(["p", "li", "div"]):
                continue
            txt = re.sub(r"\s+", " ", el.get_text(" ", strip=True))
            if len(txt) < 25:
                continue
            if any(k.lower() in txt.lower() for k in keys) and txt not in blocks:
                blocks.append(txt)
        for b in blocks[:14]:
            out.write("- " + b[:CUT] + "\n")
    except Exception as e:  # report and continue
        out.write(f"\n===== {url}\nERROR {e}\n")
out.close()
