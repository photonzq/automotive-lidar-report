"""Sanity checks on the built report PDF.

Reports: page count, pages where key sections land, pages with unrendered TeX, suspicious "$" signs,
metadata, outline size, attached files and figure paperclips. Renders the key pages (or the pages
given as arguments) as PNG into a temporary folder and prints its path.

Usage: python check_pdf.py [page numbers, 1-based ...]
"""
import re
import sys
import tempfile
from pathlib import Path

import pymupdf

HERE = Path(__file__).resolve().parent
pdf = HERE.parent / "automotive_perception_report_2026-09-27.pdf"
out = Path(tempfile.mkdtemp(prefix="report-check-"))
d = pymupdf.open(pdf)
keys = ["C0. Physics primer", "C3. Company route table", "C4d. Mechanical beam", "Figure C4d", "国科光芯",
        "Scanner-induced Doppler (mechanical", "C10.3a Physical background", "Contents", "Appendix 2",
        "Figure C3a", "C5a. Sony"]
hits, raw_tex, dollars, clips = {}, [], [], []
for i, p in enumerate(d):
    t = p.get_text()
    for k in keys:
        if k in t and k not in hits:
            hits[k] = i
    if re.search(r"\\(frac|approx|mathrm|times|lambda|theta|Delta)", t):
        raw_tex.append(i)
    for m in re.finditer(r"\$[^\d\s,.]", t):
        dollars.append((i, t[max(0, m.start() - 30):m.end() + 30].replace("\n", " ")))
    for a in p.annots() or []:
        if a.type[1] == "FileAttachment":
            clips.append((i + 1, a.file_info.get("filename")))
print("pages", d.page_count)
print("hits", hits)
print("raw tex pages", raw_tex[:20])
print("suspicious $", dollars[:15], len(dollars))
print("metadata", d.metadata)
toc = d.get_toc()
print("outline entries", len(toc), toc[:5])
print("attached files", d.embfile_count(), [d.embfile_info(k)["filename"] for k in range(d.embfile_count())])
print("figure paperclips (page, file)", clips)
pages = [int(x) - 1 for x in sys.argv[1:]] if len(sys.argv) > 1 else sorted(set(hits.values()) | {0, 1})
for i in pages:
    d[i].get_pixmap(dpi=80).save(out / f"pg_{i + 1:03d}.png")
print("rendered", [i + 1 for i in pages], "into", out)
