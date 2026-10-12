"""Render the author-supplied reference PDFs to PNG (dpi 160) and print a page index."""
import re
from pathlib import Path

import pymupdf

OUT = Path(r"<scratch>\refs")
OUT.mkdir(exist_ok=True)
DOCS = {
    "nature": r"<downloads>\s41586-026-10183-6.pdf",
    "natureSI": r"<refs folder>\soliton\41586_2026_10183_MOESM1_ESM.pdf",
    "wang": r"<downloads>\s44275-025-00030-7.pdf",
    "sony": r"<refs folder>\7.3_A_189600_Back-Illuminated_Stacked_SPAD_Direct_Time-of-Flight_Depth_Sensor_for_Automotive_LiDAR_Systems.pdf",
    "nphot": r"<refs folder>\s41566-020-0586-0.pdf",
}
for tag, path in DOCS.items():
    d = pymupdf.open(path)
    print(f"== {tag}: {d.page_count} pages; title meta: {d.metadata.get('title', '')[:120]!r}")
    for i, p in enumerate(d):
        t = re.sub(r"\s+", " ", p.get_text()).strip()
        png = OUT / f"{tag}_p{i + 1:02d}.png"
        if not png.exists():
            p.get_pixmap(dpi=160).save(png)
        print(f"  p{i + 1:02d} [{len(t):5d} ch] {t[:150]}")
