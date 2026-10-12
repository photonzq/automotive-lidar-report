"""Download a public earnings-call transcript page and print keyword contexts.

Used for the robotics-lidar items of the automotive perception report: the
RoboSense calls of 25 Mar 2026 (FY2025) and 27 May 2026 (Q1 2026) and the Hesai
calls of 24 Mar 2026 (Q4 2025), 19 May 2026 (Q1 2026) and 18 Aug 2026
(Q2 2026), whose segment remarks (mowers, robovans, humanoids, lidars per
vehicle, guidance) are not in the written filings.

The transcripts are machine or third-party transcriptions: numbers in them
must be checked against the filings (one RoboSense transcript renders Q1 2026
revenue of RMB 458.8 M as "RMB 158.8 million").

Usage
-----
    python call_transcript_grep.py URL out.txt mower robovan "two to four"

The page HTML is reduced to plain text, saved to ``out.txt`` (relative to the
working directory), and up to three 300-character contexts are printed for
each keyword. Only a generic browser User-Agent is sent.
"""
import html
import re
import sys

import requests

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124 Safari/537.36",
      "Accept-Language": "en-US,en;q=0.9"}


def page_text(url: str) -> str:
    r = requests.get(url, headers=UA, timeout=60)
    r.raise_for_status()
    t = re.sub(r"<script.*?</script>", "", r.text, flags=re.S)
    t = re.sub(r"<style.*?</style>", "", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t))


def main() -> None:
    if len(sys.argv) < 4:
        raise SystemExit(__doc__)
    url, out, kws = sys.argv[1], sys.argv[2], sys.argv[3:]
    t = page_text(url)
    with open(out, "w", encoding="utf-8") as f:
        f.write(t)
    for kw in kws:
        hits = list(re.finditer(re.escape(kw), t, flags=re.I))
        print(f"##### [{kw}] {len(hits)} hits")
        for m in hits[:3]:
            print("...", t[max(0, m.start() - 300):m.end() + 300], "\n")


if __name__ == "__main__":
    main()
