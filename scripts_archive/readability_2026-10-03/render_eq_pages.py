"""Render the PDF pages that hold given equation numbers, to check how display equations typeset.

Usage: python render_eq_pages.py OUT_DIR N [N ...]
Each page whose text contains "(N)" at a line end (the right-aligned equation number) is rendered at 110 dpi.
"""
import re
import sys
from pathlib import Path

import pymupdf

PDF = Path(r"<report folder>\automotive_perception_report_2026-09-27.pdf")
out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
doc = pymupdf.open(PDF)
for n in sys.argv[2:]:
    pat = re.compile(rf"^\({n}\)\s*$", re.M)
    for i, page in enumerate(doc):
        if pat.search(page.get_text()):
            f = out / f"eq{n}_p{i + 1}.png"
            page.get_pixmap(dpi=110).save(f)
            print(n, "page", i + 1, f)
            break
    else:
        print(n, "not found")
