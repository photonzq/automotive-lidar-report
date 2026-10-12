"""Search the downloaded Chinese PDFs (Hesai STAR prospectus?, broker report) for FMCW passages; render hit pages."""
import re
from pathlib import Path

import pymupdf

TR = Path(r"<downloads>")
OUT = Path(r"<scratch>\refs")
PAT = re.compile(r"FMCW|调频连续波|相干")
for fname, tag in (("hesai_star_prospectus_draft.pdf", "qixin"), ("broker_report.pdf", "dfcfw")):
    d = pymupdf.open(TR / fname)
    first = re.sub(r"\s+", " ", d[0].get_text())[:300]
    print(f"== {tag}: {d.page_count} pages | p1: {first}")
    n = 0
    for i, p in enumerate(d):
        t = re.sub(r"\s+", " ", p.get_text())
        hits = [t[max(0, m.start() - 160):m.end() + 200] for m in PAT.finditer(t)]
        if hits:
            n += 1
            print(f"  -- p{i + 1}: {len(hits)} hits")
            for h in hits[:4]:
                print("     ", h)
            if n <= 6:
                p.get_pixmap(dpi=150).save(OUT / f"{tag}_p{i + 1:03d}.png")
    print(f"  pages with hits: {n}")
