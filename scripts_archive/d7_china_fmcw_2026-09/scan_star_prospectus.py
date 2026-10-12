"""Hesai 2021 STAR prospectus (draft): FMCW passages outside the glossary, with page numbers; render the key pages."""
import re
from pathlib import Path

import pymupdf

PDF = Path(r"<downloads>\hesai_star_prospectus_draft.pdf")
OUT = Path(r"<scratch>\refs")
d = pymupdf.open(PDF)
# the draft's date
for i in range(0, 3):
    t = re.sub(r"\s+", " ", d[i].get_text())
    m = re.search(r"20\d\d ?年 ?\d{1,2} ?月 ?\d{1,2} ?日", t)
    if m:
        print("date on page", i + 1, ":", m.group(0))
PAT = re.compile(r"FMCW|调频连续波")
keep = []
for i, p in enumerate(d):
    if i == 18:  # glossary page
        continue
    t = re.sub(r"\s+", " ", p.get_text())
    for m in PAT.finditer(t):
        keep.append((i + 1, t[max(0, m.start() - 260):m.end() + 300]))
seen = set()
for pg, ctx in keep:
    key = (pg, ctx[200:320])
    if key in seen:
        continue
    seen.add(key)
    print(f"--- p{pg}: {ctx}")
pages = sorted({pg for pg, _ in keep})
print("pages with FMCW:", pages)
for pg in pages[:12]:
    d[pg - 1].get_pixmap(dpi=150).save(OUT / f"hesai_star_p{pg:03d}.png")
