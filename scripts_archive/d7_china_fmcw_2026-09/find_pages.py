"""Locate and render the benchmark pages of the downloaded indie whitepaper and Toshiba technical review."""
import re
from pathlib import Path

import pymupdf

TR = Path(r"<downloads>")
OUT = Path(r"<scratch>\pdfcheck")
OUT.mkdir(exist_ok=True)
jobs = [("indie_whitepaper.pdf", "indie", r"(?i)rayleigh|aperture|mW|SNR"),
        ("toshiba_technical_review.pdf", "toshiba", r"(?i)SiPM|lidar|LiDAR|mW|klux|klx")]
for fname, tag, pat in jobs:
    d = pymupdf.open(TR / fname)
    print(tag, "pages", d.page_count)
    hits = []
    for i, p in enumerate(d):
        t = p.get_text()
        n = len(re.findall(pat, t))
        if n:
            hits.append((n, i))
    hits.sort(reverse=True)
    print("  best pages (count, 0-based index):", hits[:8])
    for n, i in sorted(hits[:4], key=lambda x: x[1]):
        png = OUT / f"{tag}_p{i + 1}.png"
        d[i].get_pixmap(dpi=160).save(png)
        print("  rendered", png.name)
