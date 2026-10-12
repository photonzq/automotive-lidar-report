import sys
from pathlib import Path

import pymupdf

PDF = Path(r"<report folder>\automotive_perception_report_2026-09-27.pdf")
OUT = Path(r"<scratch>\pdfcheck")
OUT.mkdir(exist_ok=True)
d = pymupdf.open(PDF)
for s in sys.argv[1:]:
    n = int(s)  # 1-based page number
    d[n - 1].get_pixmap(dpi=100).save(OUT / f"final_p{n}.png")
    print("rendered", n)
