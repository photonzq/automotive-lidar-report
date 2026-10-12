import re
from pathlib import Path

import pandas as pd
import pymupdf

for f in (r"<downloads>\41586_2026_10183_MOESM2_ESM.xlsx", r"<downloads>\41586_2026_10183_MOESM3_ESM.xlsx"):
    x = pd.ExcelFile(f)
    print("==", Path(f).name, "sheets:", x.sheet_names)
    for sh in x.sheet_names:
        df = x.parse(sh, header=None)
        print(f"  [{sh}] shape {df.shape}; first rows:")
        print(df.head(6).to_string(max_cols=12, max_colwidth=28))

d = pymupdf.open(r"<refs folder>\soliton\41586_2026_10183_MOESM1_ESM.pdf")
kw = re.compile(r"(?i)bloom|retro|dynamic range|saturat|eye safe|eye-safe|link budget|reflectiv|200 m|Rayleigh|collimat|ToF|time-of-flight|energy per")
for i, p in enumerate(d):
    t = re.sub(r"\s+", " ", p.get_text())
    hits = [t[max(0, m.start() - 90):m.end() + 110] for m in kw.finditer(t)]
    if hits:
        print(f"--- PRF p{i + 1}: {len(hits)} hits")
        for h in hits[:6]:
            print("   ", h)
