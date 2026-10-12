import tempfile
import time
from pathlib import Path

import pymupdf

PDF = Path(r"<report folder>\automotive_perception_report_2026-09-27.pdf")
tmpd = Path(tempfile.mkdtemp(prefix="savetime-"))
for g in (1, 2):
    d = pymupdf.open(PDF)
    t0 = time.time()
    out = tmpd / f"g{g}.pdf"
    d.save(out, garbage=g, deflate=True)
    d.close()
    print(f"garbage={g}: {time.time() - t0:.1f} s, {out.stat().st_size / 1e6:.1f} MB")
print("original", PDF.stat().st_size / 1e6, "MB")
