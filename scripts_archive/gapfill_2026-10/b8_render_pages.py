"""Render the filing pages behind the §B8 robot-vacuum row to PNG (dpi 160) for reading,
and search the remaining LDROBOT filings for the 2024 dToF shipment figure.

Usage:
    python render_pages.py <pdf_dir> <out_dir>
"""
import re
import sys
from pathlib import Path

import pymupdf

PDF_DIR = Path(sys.argv[1])
OUT = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

PAGES = {
    "ldrobot/2026043000099.pdf": ("ldp", [10, 11, 36, 107, 139, 140, 141, 142, 143, 144, 148]),
    "ldrobot/2026082400450.pdf": ("ldi", [2]),
    "camsense/2026092200005.pdf": ("csp", [85, 86, 87, 88, 89, 111, 143, 144, 157, 158, 159, 188]),
}

for rel, (tag, idxs) in PAGES.items():
    d = pymupdf.open(PDF_DIR / rel)
    for i in idxs:
        d[i].get_pixmap(dpi=160).save(OUT / f"{tag}_{i:03d}.png")
    print(rel, "rendered", len(idxs))

# Where does "720" thousand dToF units in 2024 come from?
for rel in ["ldrobot/AP_sehk25120104096.pdf", "ldrobot/2026043000027.pdf", "ldrobot/2026092201543.pdf"]:
    p = PDF_DIR / rel
    if not p.exists():
        print("missing", rel)
        continue
    d = pymupdf.open(p)
    print(f"== {rel} pages={d.page_count}")
    for i in range(d.page_count):
        t = d[i].get_text()
        for m in re.finditer(r"720(,\d{3}|\.\d|\s*thousand| units)|DTOF LiDAR[^.]{0,120}(2024|2023)[^.]{0,80}units|units of DTOF", t):
            s, e = max(0, m.start() - 200), min(len(t), m.end() + 200)
            print(f"  idx {i}: ...{t[s:e]}...".replace("\n", " "))
