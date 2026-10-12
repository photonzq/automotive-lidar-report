"""Create <report>/build (PDF tools) and <report>/build/figures (figure scripts + input data).

Figure scripts and their CSV are MOVED from automotive_perception_report_figures (copy, byte-compare, then delete).
The PDF tools are COPIED from the shared scratch folder (the parallel editing pass keeps using its copy until told).
"""
import filecmp
import shutil
from pathlib import Path

REPORT = Path(r"<report folder>")
FIGS = REPORT / "automotive_perception_report_figures"
BUILD = REPORT / "build"
BFIG = BUILD / "figures"
PDFTOOLS = Path(r"<scratch>\pdf")

BFIG.mkdir(parents=True, exist_ok=True)
for name in ("build_pdf.py", "check_pdf.py", "report.css"):
    shutil.copy2(PDFTOOLS / name, BUILD / name)
    assert filecmp.cmp(PDFTOOLS / name, BUILD / name, shallow=False)
    print("copied", name)

moved = []
for src in sorted(list(FIGS.glob("*.py")) + list(FIGS.glob("*.csv"))):
    dst = BFIG / src.name
    shutil.copy2(src, dst)
    assert filecmp.cmp(src, dst, shallow=False), src
    src.unlink()
    moved.append(src.name)
print("moved", len(moved), moved)
cache = FIGS / "__pycache__"
if cache.is_dir():
    shutil.rmtree(cache)
    print("removed", cache)
print("figures folder now:", sorted(p.name for p in FIGS.iterdir()))
