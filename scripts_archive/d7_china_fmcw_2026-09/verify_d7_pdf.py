from pathlib import Path

import pymupdf

PDF = Path(r"<report folder>\automotive_perception_report_2026-09-27.pdf")
OUT = Path(r"<scratch>\pdfcheck")
OUT.mkdir(exist_ok=True)
d = pymupdf.open(PDF)
print("metadata:", {k: v for k, v in d.metadata.items() if v and k not in ("creationDate", "modDate", "format")})
hits = []
for i, p in enumerate(d):
    t = p.get_text()
    if "In-house programme since 2018" in t or "co-founders 邱纯鑫" in t or "Probably on the road as a prototype" in t:
        hits.append(i + 1)
print("pages with the new Hesai/RoboSense text:", hits)
for pg in sorted(set(hits)):
    d[pg - 1].get_pixmap(dpi=130).save(OUT / f"d7_p{pg}.png")
    print("rendered", pg)
