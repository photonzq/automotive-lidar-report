"""Download selected HKEX filings of Hesai Group (stock code 2525) listed in
hkex/titlesearch_en.json (and optionally hkex/titlesearch_zh.json), save them to hkex/,
and report pages that mention Thailand-related keywords.

Usage:
    python scripts/hkex_download.py [en|zh]

Only PDF filings whose title matches one of the TITLE_PATTERNS are downloaded.
Keyword hits are written to hkex/keyword_hits_<lang>.txt as page numbers (1-based)
with a short text context, so the relevant pages can be rendered and read.
"""
import html
import json
import os
import re
import sys
import time
import urllib.request

import pymupdf

BASE = "https://www1.hkexnews.hk"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

TITLE_PATTERNS = [
    r"GLOBAL OFFERING", r"ANNUAL REPORT", r"INTERIM REPORT", r"OVERSEAS REGULATORY",
    r"Environmental, Social", r"RESULTS", r"INSIDE INFORMATION", r"PHIP",
    r"全球發售", r"年度報告", r"年報", r"中期報告", r"海外監管", r"環境、社會", r"業績", r"內幕消息",
]
KEYWORDS = [
    "Thailand", "Thai ", "Bangkok", "Ayutthaya", "Rojana", "Southeast Asia", "South-East Asia",
    "overseas production", "overseas manufacturing", "overseas factory", "Galileo",
    "泰國", "泰国", "曼谷", "大城", "東南亞", "东南亚", "海外生產", "海外工廠", "伽利略",
]


def fetch(url, path):
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        return
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=180) as r:
        data = r.read()
    with open(path, "wb") as f:
        f.write(data)
    time.sleep(1.0)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    lang = sys.argv[1] if len(sys.argv) > 1 else "en"
    listing = json.load(open(f"hkex/titlesearch_{lang}.json", encoding="utf-8"))
    rows = json.loads(listing["result"])
    out_lines = []
    for row in rows:
        title = html.unescape(row["TITLE"]).replace("\n", " ")
        link = row["FILE_LINK"]
        if not link.lower().endswith(".pdf"):
            continue
        if not any(re.search(p, title, flags=re.I) for p in TITLE_PATTERNS):
            continue
        fname = f"hkex/{lang}_" + os.path.basename(link)
        try:
            fetch(BASE + link, fname)
        except Exception as e:  # noqa: BLE001
            print("FAILED", link, e)
            continue
        doc = pymupdf.open(fname)
        header = f"\n##### {row['DATE_TIME']} | {title[:100]} | {fname} | {doc.page_count} pages"
        print(header)
        out_lines.append(header)
        for i in range(doc.page_count):
            t = doc[i].get_text()
            for kw in KEYWORDS:
                for m in re.finditer(re.escape(kw), t, flags=re.I):
                    a, b = max(0, m.start() - 150), min(len(t), m.end() + 150)
                    ctx = re.sub(r"\s+", " ", t[a:b])
                    line = f"  p{i + 1} [{kw}] ...{ctx}..."
                    print(line)
                    out_lines.append(line)
    with open(f"hkex/keyword_hits_{lang}.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))


if __name__ == "__main__":
    main()
