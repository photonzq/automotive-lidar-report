"""Compare archived captures of Fastree3D's website (Wayback Machine) before and after
Hesai's December 2023 acquisition.

Usage:  python fastree3d_wayback_pages.py [OUT_DIR]
For the pages listed in PAGES, the script asks the Wayback CDX index for all captures
since 2023, downloads the raw HTML of each capture (the "id_" form, without the archive's
toolbar), strips markup and prints, per capture, the visible text that differs from the
previous capture of the same page. This shows whether job openings, team or news
changed after the acquisition. Raw captures are saved to OUT_DIR/wayback/.
No personal data is sent.
"""
import json
import os
import re
import sys
import time
from html import unescape

import requests

HEADERS = {"User-Agent": "research-script/1.0"}
PAGES = ["www.fastree3d.com/career/?l=opportunities", "fastree3d.com/",
         "www.fastree3d.com/about-us/"]


def text_of(html):
    html = re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    txt = re.sub(r"<[^>]+>", "\n", html)
    lines = [re.sub(r"\s+", " ", unescape(x)).strip() for x in txt.split("\n")]
    return [x for x in lines if len(x) > 2]


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "fastree3d_out"
    os.makedirs(os.path.join(out, "wayback"), exist_ok=True)
    for page in PAGES:
        cdx = requests.get("http://web.archive.org/cdx/search/cdx",
                           params={"url": page, "from": "2023", "output": "json",
                                   "fl": "timestamp,original,statuscode",
                                   "filter": "statuscode:200", "collapse": "digest"},
                           headers=HEADERS, timeout=120).json()
        prev = None
        print(f"\n######## {page}: {len(cdx) - 1} distinct captures")
        # keep at most one capture per calendar quarter, to stay inside the archive's
        # rate limits
        picked, seen_q = [], set()
        for ts, orig, _ in cdx[1:]:
            q = (ts[:4], (int(ts[4:6]) - 1) // 3)
            if q not in seen_q:
                seen_q.add(q)
                picked.append((ts, orig))
        for ts, orig in picked:
            fn = os.path.join(out, "wayback", re.sub(r"[^A-Za-z0-9]", "_", page) + f"_{ts}.html")
            if not os.path.exists(fn):
                r = None
                for wait in (3, 10, 30, 60):
                    time.sleep(wait)
                    try:
                        r = requests.get(f"https://web.archive.org/web/{ts}id_/{orig}",
                                         headers=HEADERS, timeout=120)
                        break
                    except requests.RequestException:
                        r = None
                if r is None or r.status_code != 200:
                    print(f"--- {ts}: download failed")
                    continue
                with open(fn, "w", encoding="utf-8") as f:
                    f.write(r.text)
            lines = text_of(open(fn, encoding="utf-8").read())
            if prev is None:
                print(f"--- {ts} (first capture, {len(lines)} lines)")
                for x in lines[:400]:
                    print("    ", x[:200])
            else:
                added = [x for x in lines if x not in prev]
                removed = [x for x in prev if x not in lines]
                print(f"--- {ts}: +{len(added)} / -{len(removed)} lines")
                for x in added[:60]:
                    print("    +", x[:200])
                for x in removed[:60]:
                    print("    -", x[:200])
            prev = set(lines)


if __name__ == "__main__":
    main()
