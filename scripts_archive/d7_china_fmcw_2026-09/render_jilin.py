import re
from pathlib import Path

import pymupdf

TR = Path(r"<downloads>")
OUT = Path(r"<scratch>\refs")
for fname, tag in (("jilin_oe2022.pdf", "jilin_oe2022"), ("jilin_pr2021.pdf", "jilin_pr2021")):
    d = pymupdf.open(TR / fname)
    print(tag, "pages", d.page_count)
    for i, p in enumerate(d):
        t = re.sub(r"\s+", " ", p.get_text())
        k = len(re.findall(r"(?i)\b1\d\d ?m\b|reflectiv|mirror|dBm|SNR|SPNR", t))
        if i == 0 or k >= 3:
            p.get_pixmap(dpi=160).save(OUT / f"{tag}_p{i + 1}.png")
            print(f"  rendered p{i + 1} ({k} hits): {t[:120]}")
