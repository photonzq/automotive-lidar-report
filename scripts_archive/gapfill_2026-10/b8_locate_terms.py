"""Locate the pages of the LDROBOT and Camsense HKEX filings that the two §B8 bullets cite.

Text extraction is used only to find pages; the pages are then rendered and read as images.

Usage:
    python locate_terms.py <pdf_dir> <out_txt>
"""
import re
import sys
from pathlib import Path

import pymupdf

PDF_DIR = Path(sys.argv[1])
OUT = Path(sys.argv[2])

FILES = {
    "ldrobot_prospectus": "ldrobot/2026043000099.pdf",
    "ldrobot_interim": "ldrobot/2026082400450.pdf",
    "camsense_prospectus": "camsense/2026092200005.pdf",
}

TERMS = [
    r"DTOF|dTOF|dToF",
    r"direct(ly)? (time|measur)",
    r"Series 06|Series 26|06 Series|26 Series",
    r"triangular",
    r"approximately 80(\.0)?%|80(\.0)?% of",
    r"VCSEL",
    r"SPAD",
    r"P[- ]?series|P[- ]?Series",
    r"10\.29|10,29\d,\d{3}",
    r"720,\d{3}|0\.72 million",
    r"4(\.\d+)? million|4,\d{3},\d{3}",
    r"home cleaning robot|robotic vacuum|robot vacuum|sweeping robot|floor[- ]cleaning robot",
]


def printed_page(text):
    """Guess the printed page number from the last short numeric line of the page."""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    for l in reversed(lines[-6:]):
        if re.fullmatch(r"[–\-—]?\s*\d{1,4}\s*[–\-—]?|[IVXLC]+-\d{1,4}", l):
            return l
    return "?"


with OUT.open("w", encoding="utf-8") as f:
    for key, rel in FILES.items():
        d = pymupdf.open(PDF_DIR / rel)
        f.write(f"===== {key}  {rel}  pages={d.page_count}\n")
        for i in range(d.page_count):
            t = d[i].get_text()
            hits = []
            for pat in TERMS:
                for m in re.finditer(pat, t):
                    s = max(0, m.start() - 90)
                    e = min(len(t), m.end() + 90)
                    hits.append((pat, t[s:e].replace("\n", " ")))
            if hits:
                f.write(f"--- idx {i} (printed {printed_page(t)})  hits={len(hits)}\n")
                seen = set()
                for pat, snip in hits[:12]:
                    if snip in seen:
                        continue
                    seen.add(snip)
                    f.write(f"   [{pat[:18]}] ...{snip}...\n")
        f.write("\n")
print("wrote", OUT)
