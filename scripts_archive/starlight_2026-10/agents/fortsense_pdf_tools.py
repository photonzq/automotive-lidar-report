"""Helper for the Fortsense research task.

Usage:
  python pdf_tools.py find <pdf> <keyword> [<keyword> ...]
      prints page numbers (1-based) containing each keyword and a short snippet
  python pdf_tools.py render <pdf> <pages> [dpi] [clip]
      renders the listed 1-based pages (e.g. "1,3-5") to PNG next to the PDF
      at the given dpi (default 160). Optional clip "x0,y0,x1,y1" in PDF points
      (fractions of page if all values <= 1) renders only that region.
"""
import sys
import os
import pymupdf

sys.stdout.reconfigure(encoding="utf-8")


def parse_pages(spec, n):
    pages = []
    for part in spec.split(","):
        if "-" in part:
            a, b = part.split("-")
            pages.extend(range(int(a), int(b) + 1))
        else:
            pages.append(int(part))
    return [p for p in pages if 1 <= p <= n]


def cmd_find(pdf, keywords):
    d = pymupdf.open(pdf)
    print(f"{pdf}: {d.page_count} pages")
    for kw in keywords:
        hits = []
        for i in range(d.page_count):
            t = d[i].get_text()
            j = t.find(kw)
            if j >= 0:
                hits.append(i + 1)
                snippet = t[max(0, j - 80): j + 160].replace("\n", " ")
                print(f"  [{kw}] p{i + 1}: ...{snippet}...")
        print(f"  [{kw}] pages: {hits}")


def cmd_render(pdf, spec, dpi=160, clip=None):
    d = pymupdf.open(pdf)
    base = os.path.splitext(pdf)[0]
    for p in parse_pages(spec, d.page_count):
        page = d[p - 1]
        kwargs = {"dpi": dpi}
        suffix = ""
        if clip:
            vals = [float(v) for v in clip.split(",")]
            if all(v <= 1.0 for v in vals):
                r = page.rect
                vals = [vals[0] * r.width, vals[1] * r.height,
                        vals[2] * r.width, vals[3] * r.height]
            kwargs["clip"] = pymupdf.Rect(*vals)
            suffix = "_clip" + "_".join(str(int(v)) for v in vals)
        out = f"{base}_p{p}{suffix}.png"
        page.get_pixmap(**kwargs).save(out)
        print(out)


if __name__ == "__main__":
    if sys.argv[1] == "find":
        cmd_find(sys.argv[2], sys.argv[3:])
    elif sys.argv[1] == "render":
        dpi = int(sys.argv[4]) if len(sys.argv) > 4 else 160
        clip = sys.argv[5] if len(sys.argv) > 5 else None
        cmd_render(sys.argv[2], sys.argv[3], dpi, clip)
