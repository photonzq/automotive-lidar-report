from pathlib import Path

import pymupdf

REPORT = Path(r"<report folder>")
PDF = REPORT / "automotive_perception_report_2026-09-27.pdf"
OUT = Path(r"<scratch>\pdfcheck")
OUT.mkdir(exist_ok=True)

d = pymupdf.open(PDF)
print("metadata:", {k: v for k, v in d.metadata.items() if v})
print("attachments:", [(d.embfile_info(k)["name"], d.embfile_info(k)["size"]) for k in range(d.embfile_count())])
disk = {p.name: p.read_bytes() for p in (REPORT / "build" / "figures").iterdir() if p.is_file()}
for k in range(d.embfile_count()):
    info = d.embfile_info(k)
    assert d.embfile_get(k) == disk[info["filename"]], info["filename"]
print("every attachment is byte-identical to build/figures/ on disk")
clips = []
for p in d:
    for a in p.annots() or []:
        if a.type[1] == "FileAttachment":
            clips.append((p.number + 1, a.file_info["filename"], tuple(round(v) for v in a.rect)))
            assert a.get_file() == disk[a.file_info["filename"]]
print("paperclips:", clips)
eq_page = next(i for i, p in enumerate(d) if "Link budget: loss versus range" in p.get_text() and "(1" in p.get_text())
for pno in sorted({clips[0][0] - 1, clips[5][0] - 1, eq_page, eq_page + 1}):
    d[pno].get_pixmap(dpi=110).save(OUT / f"final_p{pno + 1}.png")
    print("rendered page", pno + 1)
