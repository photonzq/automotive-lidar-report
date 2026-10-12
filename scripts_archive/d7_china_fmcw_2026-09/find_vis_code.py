import re
from pathlib import Path

import pymupdf

pdf = Path(r"<downloads>\dense_fog_paper.pdf")
out = Path(r"<scratch>\pdfcheck")
out.mkdir(exist_ok=True)
d = pymupdf.open(pdf)
print("pages", d.page_count)
hits = []
for i, p in enumerate(d):
    t = p.get_text()
    if re.search(r"(?i)thick fog|light haze|thin fog|visibility code", t):
        hits.append(i)
        print("page index", i, "(printed page", i + 1, "):", re.sub(r"\s+", " ", t)[:300])
for i in hits[:3]:
    d[i].get_pixmap(dpi=160).save(out / f"dense_p{i + 1}.png")
    print("rendered", out / f"dense_p{i + 1}.png")
