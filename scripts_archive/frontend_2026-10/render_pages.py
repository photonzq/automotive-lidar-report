"""Render selected PDF pages to PNG (160 dpi) and print page counts and a keyword locator.
Usage: python -I render_pages.py <out dir> <pdf> <pages: all | 1,2,5-7> [keyword ...]
Pages are 1-based. With keywords, also prints the pages whose text contains each keyword (to locate, not to read).
"""
import site
import sys
from pathlib import Path

sys.path.append(site.getusersitepackages())  # -I hides the user site, where PyMuPDF is installed
import pymupdf  # noqa: E402

out, pdf, spec = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
keys = sys.argv[4:]
d = pymupdf.open(pdf)
print(f"{pdf.name}: {d.page_count} pages")
for k in keys:
    hits = [i + 1 for i in range(d.page_count) if k.lower() in d[i].get_text().lower()]
    print(f"  '{k}' on pages {hits}")
if spec == "none":
    sys.exit(0)
pages = []
if spec == "all":
    pages = list(range(1, d.page_count + 1))
else:
    for part in spec.split(","):
        a, _, b = part.partition("-")
        pages += list(range(int(a), int(b or a) + 1))
out.mkdir(parents=True, exist_ok=True)
for p in pages:
    f = out / f"{pdf.stem}_p{p:02d}.png"
    d[p - 1].get_pixmap(dpi=160).save(f)
    print("rendered", f.name)
