"""Second pass: find the sales-volume tables and market-size statements behind the §B8 robot-vacuum row.

Usage:
    python locate_terms2.py <pdf_dir> <out_txt>
"""
import re
import sys
from pathlib import Path

import pymupdf

PDF_DIR = Path(sys.argv[1])
OUT = Path(sys.argv[2])

JOBS = [
    ("ldrobot/2026043000099.pdf", [r"10,29\d", r"720(\.\d)?", r"[Ss]ales volume", r"thousand units", r"[Ii]n the same year",
                                   r"units of sensors", r"shipped (approximately|over)"]),
    ("ldrobot/2026082400450.pdf", [r"10,29\d|10\.29", r"thousand units", r"[Ss]ales volume", r"shipments? (exceeded|of|reached)"]),
    ("camsense/2026092200005.pdf", [r"robotic vacuum shipments?|shipments? of robotic vacuums?|robotic vacuums? shipped",
                                    r"million units", r"penetration (rate )?of LiDAR|LiDAR penetration", r"According to CIC, approximately 80",
                                    r"Source: .*CIC|Source: IDC"]),
]

with OUT.open("w", encoding="utf-8") as f:
    for rel, pats in JOBS:
        d = pymupdf.open(PDF_DIR / rel)
        f.write(f"===== {rel} pages={d.page_count}\n")
        for i in range(d.page_count):
            t = d[i].get_text()
            out = []
            for pat in pats:
                for m in re.finditer(pat, t):
                    s = max(0, m.start() - 160)
                    e = min(len(t), m.end() + 160)
                    out.append(f"   [{pat[:22]}] ...{t[s:e]}...".replace("\n", " "))
            if out:
                f.write(f"--- idx {i}\n")
                for line in dict.fromkeys(out):
                    f.write(line + "\n")
print("wrote", OUT)
