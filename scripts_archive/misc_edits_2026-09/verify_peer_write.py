import re
from pathlib import Path

import pymupdf

REPORT = Path(r"<report folder>")
MD = REPORT / "automotive_perception_report_2026-09-27.md"
PDF = REPORT / "automotive_perception_report_2026-09-27.pdf"
PREV = Path(r"<scratch>\rewrite\report_after_attachtext.md")

raw = MD.read_bytes()
s = raw.decode("utf-8")
print("bytes", len(raw), "| CR present:", b"\r" in raw, "| tabs:", b"\t" in raw)
odd = [i for i, l in enumerate(s.split("\n"), 1) if l.replace("\\$", "").count("$") % 2]
print("odd-$ lines:", odd[:10])
tags = [int(x) for x in re.findall(r"\\tag\{(\d+)\}", s)]
print("tags:", len(tags), "contiguous 1..N in order:", tags == list(range(1, len(tags) + 1)))
disp = len(re.findall(r"\$\$(.+?)\$\$", s, flags=re.S))
print("display equations:", disp, "| untagged:", disp - len(tags))
refs = []
for m in re.finditer(r"\bEqs?\.\s*\(\d+\)(?:\s*(?:,|and|–|-|to|or)\s*\(\d+\))*", s):
    refs += [int(x) for x in re.findall(r"\((\d+)\)", m.group(0))]
print("Eq. references:", len(refs), "| dangling:", sorted({r for r in refs if r < 1 or r > len(tags)}))
print("leftover eq: labels:", len(re.findall(r"eq:[a-z0-9]", s)))
prev = PREV.read_text(encoding="utf-8")
hs = lambda t: [l for l in t.split("\n") if re.match(r"^#{1,4} ", l)]
print("headings unchanged vs the previous version:", hs(s) == hs(prev))
src = lambda t: [l for l in t.split("\n") if l.startswith("Sources:")]
print("Sources: lines unchanged:", src(s) == src(prev))

d = pymupdf.open(PDF)
print("PDF pages", d.page_count, "| attachments", d.embfile_count(),
      "| paperclips", sum(1 for p in d for a in (p.annots() or []) if a.type[1] == "FileAttachment"),
      "| metadata", {k: v for k, v in d.metadata.items() if v and k not in ("format",)})
